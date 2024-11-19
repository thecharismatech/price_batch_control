Odoo 17 v/s Odoo 18: Technical Side Comparison Report
1. Chatter
Odoo 17:

<div class="oe_chatter">
   <field name="message_follower_ids"/>
   <field name="activity_ids"/>
   <field name="message_ids"/>
</div>
Odoo 18:

<chatter/>
2. Tree/List View
Odoo 17:

* Used Tree view.

Given the example below. 

<tree editable="bottom" create="false">
   <field name="employee_id" column_invisible="1"/>
   <field name="filename" column_invisible="1"/>
   <field name="finger_id" create="false" edit="false"/>
   <field name="finger_template" create="false" widget="binary" filename="filename"/>
</tree>
* Given tree in Actions for tree view

<field name="view_mode">tree</field>
Odoo 18:

* Changed into list view

<list>
   <field name="name"/>
   <field name="widget_type"/>
   <field name="size_x"/>
   <field name="size_y"/>
   <field name="sequence" widget="handle"/>
</list>
<field name="view_mode">list</field>
3. Changes In Schedule Actions
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

* Removed the numbercall.

<record id="autovacuum_job" model="ir.cron">
   <field name="name">Base: Auto-vacuum internal data</field>
   <field name="model_id" ref="model_ir_autovacuum"/>
   <field name="state">code</field>
   <field name="code">model._run_vacuum_cleaner()</field>
   <field name='interval_number'>1</field>
   <field name='interval_type'>days</field>
   <field name="priority">3</field>
</record>
4. Read-Only Decorator
Odoo 17:

* Default Decorators like depends, onchange, constrains, returns, etc.

Odoo 18:

* Added a new decorator readonly.

@api.readonly
def activity_format(self):
   return Store(self).get_result()
5. Name Search
Odoo 17:

* _name_search: This method was traditionally used to search a model's records based on the user's input in the UI. It typically returns a list of matching records, but its functionality was somewhat limited and tied to the _name field of a model, meaning it could only search basic name fields.

def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
   if operator in ("ilike", "like"):
       name = AccountTax._parse_name_search(name)
   return super()._name_search(name, domain, operator, limit, order)
Odoo 18:

* _search_display_name: With Odoo 18, _search_display_name expands upon the capabilities of _name_search. It allows for more advanced searches and is no longer restricted to just the _name field. This method can provide more flexibility by searching across various fields, improving user experience when interacting with the system's search capabilities.

def _search_display_name(self, operator, value):
   domain = []
   if operator != 'ilike' or (value or '').strip():
       criteria_operator = ['|'] if operator not in expression.NEGATIVE_TERM_OPERATORS else ['&', '!']
       name_domain = criteria_operator + [('code_prefix_start', '=ilike', value + '%'), ('name', operator, value)]
       domain = expression.AND([name_domain, domain])
   return domain
6. Access Rights/Rules
Odoo 17:

* check_access_rights() for access rights and check_access_rule() for access rules. These must be called independently.

self.check_access_rights('read')
self.check_access_rule('read')
* Conditional Return Types: Depending on the parameters passed (like whether checking for read, write, or create permissions), the return types can vary, adding complexity to the code.

article.user_has_access = article.user_permission != 'none' if article.user_permission else False
* _filter_access_rule(): This method filters access based on rules but doesn't integrate access rights checks.

Model._filter_access_rules('read')
Odoo 18:

* check_access(): A single method that handles both access rights and rules. It simplifies access control checks by reducing the number of method calls required, even when dealing with empty recordsets. This ensures that security is enforced consistently without needing separate checks.

record.check_access("read")
* has_access() Method: A new method returns a simple boolean value, making it easier to integrate access checks into the business logic.

display_link = record.has_access('read')
* _filtered_access(): This replaces _filter_access_rule() and _filter_access_rule_python(). The method now checks both access rights and rules in one go, returning an empty recordset if the user doesn't have access to the model.

valid_records = self._filtered_access('write')
7. Translation function  _()
Odoo 17:

* The _() function relies on inspecting the caller’s stack, which can lead to occasional issues with language and module resolution.

raise ValidationError(_('Invalid model name %r in action definition.', action.res_model))
Odoo 18:

* The env._() function simplifies translation by directly using the environment’s language property. The LazyTranslate factory also improves efficiency, particularly for lazy translations.

raise UserError(self.env._("You cannot invoice a refund whose linked order hasn't been invoiced."))
8.  SQL Operator Change in _search Functions
Odoo 17:

* The internal SQL operator inselect is used in the _search functions. This operator is specific to Odoo and is used for performing checks on lists of values within SQL queries.

* While functional, this approach is less standard and can be harder to read or maintain.

if (operator == '=' and value is True) or (operator == '!=' and value is False):
   operator_new = 'inselect'
else:
   operator_new = 'not inselect'
Odoo 18:

* Replaces inselect with the standard SQL IN clause. This change simplifies the SQL queries by making them more intuitive and easier to understand.

* Using the IN clause is a more efficient and universally recognized practice in SQL, improving both query readability and performance.

9.  Date Granularity in Reporting
Odoo 17:

* Limited to "absolute" date granularities like Year, Quarter, Month, Week, and Day.

Odoo 18:

* Adds more flexible grouping by introducing month_number, quarter_number, and week_number, allowing for date grouping across different years.

* This enhancement in Odoo 18 offers more flexibility and control when working with date-based reports.

* The new granularities can be used in read_group or _read_group to group data by these new date fields (e.g., date_field:month_number).

* You can also filter by specific months, quarters, or weeks in the domain. For instance, ('date_field.month_number', '=', 2) would return all data for February, regardless of the year.

result = self.env["test_new_api.person"].search([('birthday.month_number', '=', '2')])
10.   Grouping and Sorting of Related Fields
Odoo 17:

*  Related fields had to be stored to be grouped, aggregated, or sorted.

* The group_operator attribute of the field.

Odoo 18:

* It is now possible to group/aggregate/sort by a no-store-related field. It is only possible for those that have related_sudo=True (or compute_sudo=True), but it targets the majority of them.

* Create a new groupable description attribute on the Field class. Also, modify the existing _description_sortable and _description_group_operator to take in account related no-store fields.

self.assertFalse(field_info['foo_id_name']['groupable'])
* The group_operator attribute of the field is renamed into aggregator

allocated_percentage = fields.Float("Allocated Time (%)", readonly=True, aggregator="avg")
11. Deprecation of _flush_search() Method
Odoo 17:

* Utilizes _flush_search() for flushing fields during search queries.

self.env['project.task']._flush_search(task_specific_domain, fields=self.task_specific_fields)
Odoo 18:

* Deprecates _flush_search() and delegates flushing to execute_query(), improving the ORM's internal efficiency and access rights checks.

placeholder_codes = self.env.execute_query(query_account.select(placeholder_code_alias))
12. Rpc Method In js
Odoo 17:

* Used jsonrpc for making RPC calls

import { jsonrpc } from "@web/core/network/rpc_service";
Odoo 18:

* Introduces the more streamlined rpc method, removing the need to handle jsonrpc directly.

import { rpc } from "@web/core/network/rpc";