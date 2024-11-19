from odoo import models, fields, api
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    price_change_count = fields.Integer(compute='_compute_price_change_count')
    price_change_ids = fields.One2many('price.change.log', 'product_id', string='Price Changes')

    def _compute_price_change_count(self):
        for product in self:
            product.price_change_count = len(product.price_change_ids)

    def action_view_price_changes(self):
        self.ensure_one()
        return {
            'name': 'Price Changes',
            'type': 'ir.actions.act_window',
            'res_model': 'price.change.log',
            'view_mode': 'tree,form',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id},
        }