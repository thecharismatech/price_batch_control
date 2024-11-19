from odoo import api, fields, models, _ 
from odoo.exceptions import UserError 
 
class PriceChange(models.Model): 
    _name = 'price.change' 
    _description = 'Price Change Request' 
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
 
    name = fields.Char(string='Reference', required=True, readonly=True, default=lambda self: _('New'), tracking=True) 
    date = fields.Datetime(string='Change Date', default=fields.Datetime.now, tracking=True) 
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('approved', 'Approved')], default='draft', tracking=True) 
    change_type = fields.Selection([('percentage', '%'), ('fixed', 'Fixed')], required=True, tracking=True) 
    change_value = fields.Float(string='Value', required=True, tracking=True) 
    product_ids = fields.Many2many('product.product', string='Products', tracking=True) 
 
    @api.model_create_multi 
    def create(self, vals_list): 
        for vals in vals_list: 
            if vals.get('name', _('New')) == _('New'): 
                vals['name'] = self.env['ir.sequence'].next_by_code('price.change') or _('New') 
        return super().create(vals_list) 
