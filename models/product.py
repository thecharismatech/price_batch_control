from odoo import models, fields, api
from odoo.osv import expression

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    price_change_count = fields.Integer(compute='_compute_price_change_count', aggregator="count")
    price_change_ids = fields.One2many('price.change.log', 'product_id', string='Price Changes')
    service_to_purchase = fields.Boolean(string='Service to Purchase', default=False)

    def _compute_price_change_count(self):
        for product in self:
            product.price_change_count = len(product.price_change_ids)

    def _search_display_name(self, operator, value):
        domain = []
        if operator != 'ilike' or (value or '').strip():
            criteria_operator = ['|'] if operator not in expression.NEGATIVE_TERM_OPERATORS else ['&', '!']
            name_domain = criteria_operator + [
                ('default_code', '=ilike', value + '%'),
                ('name', operator, value)
            ]
            domain = expression.AND([name_domain, domain])
        return domain

    @api.readonly
    def action_view_price_changes(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Price Changes'),
            'res_model': 'price.change.log',
            'view_mode': 'list,form',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id},
        }
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_open_price_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Change Prices',
            'res_model': 'price.change.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_source': 'purchase',
                'default_source_document_id': f'purchase.order,{self.id}',
                'default_product_ids': self.order_line.mapped('product_id.product_tmpl_id').ids
            }
        }

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_price_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Change Prices',
            'res_model': 'price.change.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_source': 'picking',
                'default_source_document_id': f'stock.picking,{self.id}',
                'default_product_ids': self.move_ids.mapped('product_id.product_tmpl_id').ids
            }
        }

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_count = fields.Integer(compute='_compute_purchase_order_count', aggregator="count")

    def _compute_purchase_order_count(self):
        for order in self:
            order.purchase_order_count = self.env['purchase.order'].search_count([
                ('origin', '=', order.name)
            ])

    def action_open_price_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Change Prices',
            'res_model': 'price.change.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_source': 'sale',
                'default_source_document_id': f'sale.order,{self.id}',
                'default_product_ids': self.order_line.mapped('product_id.product_tmpl_id').ids
            }
        }
