from odoo import models, fields, api, _
from odoo.osv import expression

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    price_change_count = fields.Integer(compute='_compute_price_change_count')
    price_change_ids = fields.One2many('price.change.log', 'product_id', string='Price Changes')

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

    def action_view_price_changes(self):
        self.ensure_one()
        return {
            'name': _('Price Changes'),
            'type': 'ir.actions.act_window',
            'res_model': 'price.change.log',
            'view_mode': 'list,form',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id},
        }