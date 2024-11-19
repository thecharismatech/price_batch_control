from odoo import models, fields, api
from odoo.exceptions import UserError

class PriceChangeLog(models.Model):
    _name = 'price.change.log'
    _description = 'Price Change History'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(required=True, tracking=True)
    product_id = fields.Many2one('product.template', required=True, tracking=True)
    old_price = fields.Float(readonly=True, tracking=True)
    new_price = fields.Float(readonly=True, tracking=True)
    change_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], required=True, tracking=True)
    change_value = fields.Float(required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)
    date_approved = fields.Datetime(readonly=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def action_approve(self):
        for record in self:
            record.product_id.list_price = record.new_price
            record.state = 'approved'