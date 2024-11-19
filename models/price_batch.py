from odoo import api, fields, models
from odoo.exceptions import UserError

class PriceBatchControl(models.Model):
    _name = 'price.batch.control'
    _description = 'Price Batch Control'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, readonly=True, default=lambda self: 'New', tracking=True)
    date = fields.Datetime(string='Change Date', default=fields.Datetime.now, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved')
    ], default='draft', tracking=True)
    change_type = fields.Selection([
        ('percentage', '%'),
        ('fixed', 'Fixed')
    ], required=True, default='percentage', tracking=True)
    change_value = fields.Float(string='Value', required=True, tracking=True)
    purchase_order_ids = fields.Many2many('purchase.order', string='Purchase Orders', tracking=True)
    product_ids = fields.Many2many('product.product', string='Products', compute='_compute_products', store=True)

    @api.depends('purchase_order_ids')
    def _compute_products(self):
        for record in self:
            products = record.purchase_order_ids.mapped('order_line.product_id')
            record.product_ids = [(6, 0, products.ids)]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('price.batch.control') or 'New'
        return super().create(vals_list)

    def action_to_pending(self):
        self._filtered_access()
        for record in self:
            if not record.purchase_order_ids:
                raise UserError('Please select at least one purchase order.')
        self.write({'state': 'pending'})

    def action_approve(self):
        self._filtered_access()
        for record in self:
            if record.state != 'pending':
                raise UserError('Only pending requests can be approved.')
            if record.change_type != 'percentage':
                raise UserError('Only percentage changes are allowed.')
            
            for product in record.product_ids:
                new_price = product.standard_price * (1 + record.change_value / 100)
                product.write({'standard_price': new_price})
            record.write({'state': 'approved'})

    def _filtered_access(self):
        if not self.env.user.has_group('price_batch_control.group_price_batch_manager'):
            raise UserError('Only managers can perform this action.')

