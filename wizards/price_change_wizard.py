from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PriceChangeWizard(models.TransientModel):
    _name = 'price.change.wizard'
    _description = 'Batch Price Change Wizard'

    source = fields.Selection([
        ('manual', 'Manual Selection'),
        ('purchase', 'Purchase Order'),
        ('sale', 'Sales Order'),
        ('picking', 'Stock Transfer')
    ], string='Source', default='manual', required=True)
    source_document_id = fields.Reference(selection=[
        ('purchase.order', 'Purchase Order'),
        ('sale.order', 'Sales Order'),
        ('stock.picking', 'Stock Transfer')
    ], string='Source Document')
    change_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], required=True)
    change_value = fields.Float(string='Change Value', required=True)
    product_ids = fields.Many2many('product.template', string='Products')
    effective_date = fields.Date(string='Effective Date', required=True, default=fields.Date.today)

    @api.onchange('source', 'source_document_id')
    def _onchange_source(self):
        if self.source != 'manual' and self.source_document_id:
            if self.source == 'purchase':
                self.product_ids = self.source_document_id.order_line.mapped('product_id.product_tmpl_id')
            elif self.source == 'sale':
                self.product_ids = self.source_document_id.order_line.mapped('product_id.product_tmpl_id')
            elif self.source == 'picking':
                self.product_ids = self.source_document_id.move_ids.mapped('product_id.product_tmpl_id')

    def action_apply_changes(self):
        logs = self.env['price.change.log']
        created_logs = []
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
                'source': self.source,
                'state': 'pending'
            })
            created_logs.append(log.id)
            
        return {
            'type': 'ir.actions.act_window',
            'name': 'Price Change Logs',
            'res_model': 'price.change.log',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', created_logs)],
        }