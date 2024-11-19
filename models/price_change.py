from odoo import api, fields, models
from odoo.exceptions import UserError 
 
class PriceChange(models.Model): 
    _name = 'price.change' 
    _description = 'Price Change Request' 
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
 
    name = fields.Char(string='Reference', required=True, readonly=True, default=lambda self: self.env._('New'), tracking=True) 
    date = fields.Datetime(string='Change Date', default=fields.Datetime.now, tracking=True) 
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('approved', 'Approved')], default='draft', tracking=True) 
    change_type = fields.Selection([('percentage', '%'), ('fixed', 'Fixed')], required=True, tracking=True) 
    change_value = fields.Float(string='Value', required=True, tracking=True) 
    product_ids = fields.Many2many('product.product', string='Products', tracking=True) 
 
    @api.model_create_multi 
    def create(self, vals_list): 
        for vals in vals_list: 
            if vals.get('name', self.env._('New')) == self.env._('New'): 
                vals['name'] = self.env['ir.sequence'].next_by_code('price.change') or self.env._('New') 
        return super().create(vals_list)

    def action_approve(self):
        for record in self:
            if record.state != 'pending':
                raise UserError(self.env._('Only pending requests can be approved.'))
            for product in record.product_ids:
                if record.change_type == 'percentage':
                    new_price = product.standard_price * (1 + record.change_value / 100)
                else:
                    new_price = product.standard_price + record.change_value
                product.write({'standard_price': new_price})
            record.write({'state': 'approved'})

