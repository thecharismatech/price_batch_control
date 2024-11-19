Odoo 17 vs Odoo 18: Technical Changes Guide

1. Chatter Component
Odoo 17:

<div class="oe_chatter">
   <field name="message_follower_ids"/>
   <field name="activity_ids"/>
   <field name="message_ids"/>
</div>


Odoo 18:

<chatter/>


2. View Type Changes
Odoo 17:

<!-- Tree View -->
<tree editable="bottom" create="false">
   <field name="employee_id" column_invisible="1"/>
   <field name="filename" column_invisible="1"/>
   <field name="finger_id" create="false" edit="false"/>
   <field name="finger_template" create="false" widget="binary" filename="filename"/>
</tree>

<!-- Action Definition -->
<field name="view_mode">tree</field>


Odoo 18:

<!-- List View -->
<list>
   <field name="name"/>
   <field name="widget_type"/>
   <field name="size_x"/>
   <field name="size_y"/>
   <field name="sequence" widget="handle"/>
</list>

<!-- Action Definition -->
<field name="view_mode">list</field>


3. Scheduled Actions
Odoo 17:

<record id="autovacuum_job" model="ir.cron">
   <field name="name">Base: Auto-vacuum internal data</field>
   <field name="model_id" ref="model_ir_autovacuum"/>
   <field name="state">code</field>
   <field name="code">model._run_vacuum_cleaner()</field>
   <field name='interval_number'>1</field>
   <field name='interval_type'>days</field>
   <field name="numbercall">-1</field>
   <field name="priority">3</field>
</record>


Odoo 18:

<record id="autovacuum_job" model="ir.cron">
   <field name="name">Base: Auto-vacuum internal data</field>
   <field name="model_id" ref="model_ir_autovacuum"/>
   <field name="state">code</field>
   <field name="code">model._run_vacuum_cleaner()</field>
   <field name='interval_number'>1</field>
   <field name='interval_type'>days</field>
   <field name="priority">3</field>
</record>


4. API Decorators
Odoo 18 New Feature:

@api.readonly
def activity_format(self):
    return Store(self).get_result()


5. Record Search Methods
Odoo 17:

def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
    if operator in ("ilike", "like"):
        name = AccountTax._parse_name_search(name)
    return super()._name_search(name, domain, operator, limit, order)


Odoo 18:

def _search_display_name(self, operator, value):
    domain = []
    if operator != 'ilike' or (value or '').strip():
        criteria_operator = ['|'] if operator not in expression.NEGATIVE_TERM_OPERATORS else ['&', '!']
        name_domain = criteria_operator + [
            ('code_prefix_start', '=ilike', value + '%'),
            ('name', operator, value)
        ]
        domain = expression.AND([name_domain, domain])
    return domain


6. Access Control
Odoo 17:

# Separate checks
self.check_access_rights('read')
self.check_access_rule('read')

# Permission check
article.user_has_access = article.user_permission != 'none' if article.user_permission else False

# Filter records
Model._filter_access_rules('read')


Odoo 18:

# Combined check
record.check_access("read")

# Simple boolean check
display_link = record.has_access('read')

# Filtered access
valid_records = self._filtered_access('write')


7. Translation System
Odoo 17:

raise ValidationError(_('Invalid model name %r in action definition.', action.res_model))


Odoo 18:

raise UserError(self.env._("You cannot invoice a refund whose linked order hasn't been invoiced."))


8. SQL Operations
Odoo 18:
- Replaced custom 'inselect' operator with standard SQL IN clause
- Improved query readability and performance

9. Date Handling
Odoo 18:

# New date grouping features
result = self.env["test_new_api.person"].search([('birthday.month_number', '=', '2')])


10. Field Properties
Odoo 18:

# Field definition with aggregator
allocated_percentage = fields.Float("Allocated Time (%)", readonly=True, aggregator="avg")


11. Database Operations
Odoo 18:

# Modern query execution
placeholder_codes = self.env.execute_query(query_account.select(placeholder_code_alias))


12. JavaScript RPC
Odoo 17:

import { jsonrpc } from "@web/core/network/rpc_service";


Odoo 18:

import { rpc } from "@web/core/network/rpc";