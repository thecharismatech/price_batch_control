from odoo import models, fields, api

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
    change_value = fields.Float(string='Change Value', required=True, aggregator="sum")
    product_ids = fields.Many2many('product.template', string='Products')
    effective_date = fields.Date(string='Effective Date', required=True, default=fields.Date.today)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.onchange('source', 'source_document_id')
    def _onchange_source(self):
        if self.source != 'manual' and self.source_document_id:
            if self.source == 'purchase':
                self.product_ids = self.source_document_id.order_line.mapped('product_id.product_tmpl_id')
            elif self.source == 'sale':
                self.product_ids = self.source_document_id.order_line.mapped('product_id.product_tmpl_id')
            elif self.source == 'picking':
                self.product_ids = self.source_document_id.move_ids.mapped('product_id.product_tmpl_id')

    @api.readonly
    def action_apply_changes(self):
        if not self.product_ids:
            raise self.env._("Please select at least one product.")
            
        valid_products = self.product_ids._filtered_access('write')
        if not valid_products:
            raise self.env._("You don't have access to modify the selected products.")
            
        logs = self.env['price.change.log']
        created_logs = []
        
        for product in valid_products:
            old_price = product.list_price
            if self.change_type == 'percentage':
                new_price = old_price * (1 + self.change_value / 100)
            else:
                new_price = old_price + self.change_value
            
            if new_price < 0:
                raise self.env._("New price for %s would be negative.", product.name)
                
            log_vals = {
                'name': f'Price Change for {product.name}',
                'product_id': product.id,
                'old_price': old_price,
                'new_price': new_price,
                'change_type': self.change_type,
                'change_value': self.change_value,
                'source': self.source,
                'state': 'pending',
                'company_id': self.company_id.id,
            }
            created_logs.append(logs.create(log_vals).id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Price Change Logs',
            'res_model': 'price.change.log',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created_logs)],
            'target': 'current',
        }