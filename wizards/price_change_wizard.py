from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PriceChangeWizard(models.TransientModel):
    _name = 'price.change.wizard'
    _description = 'Batch Price Change Wizard'

    change_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], required=True)
    change_value = fields.Float(string='Change Value', required=True)
    product_ids = fields.Many2many('product.template', string='Products')
    effective_date = fields.Date(string='Effective Date', required=True, default=fields.Date.today)
    
    def action_apply_changes(self):
        logs = self.env['price.change.log']
        for product in self.product_ids:
            old_price = product.list_price
            if self.change_type == 'percentage':
                new_price = old_price * (1 + self.change_value / 100)
            else:
                new_price = old_price + self.change_value
                
            log = logs.create({
                'name': f'Price Update: {product.name}',
                'product_id': product.id,
                'old_price': old_price,
                'new_price': new_price,
                'change_type': self.change_type,
                'change_value': self.change_value,
                'state': 'pending'
            })
            
        return {
            'type': 'ir.actions.act_window',
            'name': 'Price Change Logs',
            'res_model': 'price.change.log',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', logs.ids)],
        }
