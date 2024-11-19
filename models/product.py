from odoo import models, fields, api
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    price_change_count = fields.Integer(compute='_compute_price_change_count')

    def _compute_price_change_count(self):
        for product in self:
            product.price_change_count = self.env['price.change.log'].search_count([('product_ids', 'in', product.id)])
