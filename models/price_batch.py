from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PriceBatchControl(models.Model):
    _name = 'price.batch.control'
    _description = 'Price Batch Control'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Reference', 
        required=True, 
        readonly=True, 
        default=lambda self: _('New'), 
        tracking=True
    )
    date = fields.Datetime(
        string='Change Date', 
        default=fields.Datetime.now, 
        tracking=True,
        index=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True, copy=False)
    
    change_type = fields.Selection([
        ('percentage', '%'),
        ('fixed', 'Fixed')
    ], required=True, default='percentage', tracking=True)
    
    change_value = fields.Float(
        string='Value', 
        required=True, 
        tracking=True,
        digits='Product Price'
    )
    
    purchase_order_ids = fields.Many2many(
        'purchase.order', 
        string='Purchase Orders', 
        tracking=True,
        domain="[('state', 'in', ['draft', 'sent'])]"
    )
    
    product_ids = fields.Many2many(
        'product.product', 
        string='Products', 
        compute='_compute_products', 
        store=True
    )
    
    company_id = fields.Many2one(
        'res.company', 
        string='Company',
        required=True, 
        default=lambda self: self.env.company
    )
    
    user_id = fields.Many2one(
        'res.users', 
        string='Responsible',
        default=lambda self: self.env.user,
        tracking=True
    )

    @api.depends('purchase_order_ids.order_line.product_id')
    def _compute_products(self):
        for record in self:
            products = record.purchase_order_ids.mapped('order_line.product_id')
            record.product_ids = [(6, 0, products.ids)]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('price.batch.control') or _('New')
        return super().create(vals_list)

    def action_to_pending(self):
        self.ensure_one()
        if not self.purchase_order_ids:
            raise UserError(_('Please select at least one purchase order.'))
        return self.write({'state': 'pending'})

    def action_approve(self):
        self.ensure_one()
        if self.state != 'pending':
            raise UserError(_('Only pending requests can be approved.'))
            
        for order in self.purchase_order_ids:
            for line in order.order_line:
                if self.change_type == 'percentage':
                    line.price_unit *= (1 + self.change_value / 100)
                else:
                    line.price_unit += self.change_value
                    
        return self.write({'state': 'approved'})
        
    def action_cancel(self):
        return self.write({'state': 'cancelled'})
        
    def action_reset_to_draft(self):
        return self.write({'state': 'draft'})
        
    @api.constrains('change_value')
    def _check_change_value(self):
        for record in self:
            if record.change_type == 'percentage' and (record.change_value < -100 or record.change_value > 100):
                raise UserError(_('Percentage value must be between -100 and 100'))

    def unlink(self):
        if any(record.state not in ('draft', 'cancelled') for record in self):
            raise UserError(_('You can only delete draft or cancelled records'))
        return super().unlink()