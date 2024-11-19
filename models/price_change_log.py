from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError
from odoo.osv import expression

class PriceChangeLog(models.Model):
    _name = 'price.change.log'
    _description = 'Price Change History'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(required=True, tracking=True)
    product_id = fields.Many2one('product.template', required=True, tracking=True)
    old_price = fields.Float(readonly=True, tracking=True, aggregator="avg")
    new_price = fields.Float(readonly=True, tracking=True, aggregator="avg")
    change_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], required=True, tracking=True)
    change_value = fields.Float(required=True, tracking=True, aggregator="sum")
    source = fields.Selection([
        ('manual', 'Manual Selection'),
        ('purchase', 'Purchase Order'),
        ('sale', 'Sales Order'),
        ('picking', 'Stock Transfer')
    ], string='Source', default='manual', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)
    date = fields.Datetime(string='Date', readonly=True, default=fields.Datetime.now)
    date_approved = fields.Datetime(readonly=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.readonly
    def action_approve(self):
        self.ensure_one()
        if not self.has_access('write'):
            raise UserError(self.env._("Access Denied"))
        self.product_id.list_price = self.new_price
        self.write({
            'state': 'approved',
            'date_approved': fields.Datetime.now()
        })

    def action_reject(self):
        self.ensure_one()
        self.write({'state': 'rejected'})

    def _search_display_name(self, operator, value):
        domain = []
        if operator != 'ilike' or (value or '').strip():
            criteria_operator = ['|'] if operator not in expression.NEGATIVE_TERM_OPERATORS else ['&', '!']
            name_domain = criteria_operator + [
                ('name', operator, value),
                ('product_id.name', operator, value)
            ]
            domain = expression.AND([name_domain, domain])
        return domain