@echo off
SET MODULE_PATH=price_management

REM Create main module directory and subdirectories
mkdir %MODULE_PATH%
mkdir %MODULE_PATH%\models
mkdir %MODULE_PATH%\security
mkdir %MODULE_PATH%\views

REM Create __init__.py files
echo from . import models > %MODULE_PATH%\__init__.py
echo from . import price_change > %MODULE_PATH%\models\__init__.py

REM Create main model file with all classes
echo from odoo import api, fields, models, _ > %MODULE_PATH%\models\price_change.py
echo from odoo.exceptions import UserError >> %MODULE_PATH%\models\price_change.py
echo. >> %MODULE_PATH%\models\price_change.py
echo class PriceChange(models.Model): >> %MODULE_PATH%\models\price_change.py
echo     _name = 'price.change' >> %MODULE_PATH%\models\price_change.py
echo     _description = 'Price Change Request' >> %MODULE_PATH%\models\price_change.py
echo     _inherit = ['mail.thread', 'mail.activity.mixin'] >> %MODULE_PATH%\models\price_change.py
echo. >> %MODULE_PATH%\models\price_change.py
echo     name = fields.Char(string='Reference', required=True, readonly=True, default=lambda self: _('New'), tracking=True) >> %MODULE_PATH%\models\price_change.py
echo     date = fields.Datetime(string='Change Date', default=fields.Datetime.now, tracking=True) >> %MODULE_PATH%\models\price_change.py
echo     state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('approved', 'Approved')], default='draft', tracking=True) >> %MODULE_PATH%\models\price_change.py
echo     change_type = fields.Selection([('percentage', '%%'), ('fixed', 'Fixed')], required=True, tracking=True) >> %MODULE_PATH%\models\price_change.py
echo     change_value = fields.Float(string='Value', required=True, tracking=True) >> %MODULE_PATH%\models\price_change.py
echo     product_ids = fields.Many2many('product.product', string='Products', tracking=True) >> %MODULE_PATH%\models\price_change.py
echo. >> %MODULE_PATH%\models\price_change.py
echo     @api.model_create_multi >> %MODULE_PATH%\models\price_change.py
echo     def create(self, vals_list): >> %MODULE_PATH%\models\price_change.py
echo         for vals in vals_list: >> %MODULE_PATH%\models\price_change.py
echo             if vals.get('name', _('New')) == _('New'): >> %MODULE_PATH%\models\price_change.py
echo                 vals['name'] = self.env['ir.sequence'].next_by_code('price.change') or _('New') >> %MODULE_PATH%\models\price_change.py
echo         return super().create(vals_list) >> %MODULE_PATH%\models\price_change.py

REM Create manifest file
echo { > %MODULE_PATH%\__manifest__.py
echo     'name': 'Price Management', >> %MODULE_PATH%\__manifest__.py
echo     'version': '18.0.1.0.0', >> %MODULE_PATH%\__manifest__.py
echo     'category': 'Sales', >> %MODULE_PATH%\__manifest__.py
echo     'summary': 'Manage product price changes', >> %MODULE_PATH%\__manifest__.py
echo     'author': 'Mahmoud Osama - Maxmatech', >> %MODULE_PATH%\__manifest__.py
echo     'website': 'http://www.maxmatech.com', >> %MODULE_PATH%\__manifest__.py
echo     'license': 'LGPL-3', >> %MODULE_PATH%\__manifest__.py
echo     'depends': ['base', 'sale_management', 'purchase', 'mail'], >> %MODULE_PATH%\__manifest__.py
echo     'data': [ >> %MODULE_PATH%\__manifest__.py
echo         'security/ir.model.access.csv', >> %MODULE_PATH%\__manifest__.py
echo         'data/price_change_sequence.xml', >> %MODULE_PATH%\__manifest__.py
echo         'views/price_change_views.xml', >> %MODULE_PATH%\__manifest__.py
echo     ], >> %MODULE_PATH%\__manifest__.py
echo     'installable': True, >> %MODULE_PATH%\__manifest__.py
echo     'application': True, >> %MODULE_PATH%\__manifest__.py
echo     'auto_install': False, >> %MODULE_PATH%\__manifest__.py
echo } >> %MODULE_PATH%\__manifest__.py

REM Create security file
echo id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink > %MODULE_PATH%\security\ir.model.access.csv
echo access_price_change_user,price.change,model_price_change,sales_team.group_sale_salesman,1,1,1,0 >> %MODULE_PATH%\security\ir.model.access.csv
echo access_price_change_manager,price.change,model_price_change,sales_team.group_sale_manager,1,1,1,1 >> %MODULE_PATH%\security\ir.model.access.csv

REM Create sequence data file
mkdir %MODULE_PATH%\data
echo ^<?xml version="1.0" encoding="utf-8"?^> > %MODULE_PATH%\data\price_change_sequence.xml
echo ^<odoo^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo     ^<data noupdate="1"^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo         ^<record id="seq_price_change" model="ir.sequence"^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo             ^<field name="name"^>Price Change Sequence^</field^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo             ^<field name="code"^>price.change^</field^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo             ^<field name="prefix"^>PC/^</field^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo             ^<field name="padding"^>5^</field^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo         ^</record^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo     ^</data^> >> %MODULE_PATH%\data\price_change_sequence.xml
echo ^</odoo^> >> %MODULE_PATH%\data\price_change_sequence.xml

REM Create view file
echo ^<?xml version="1.0" encoding="utf-8"?^> > %MODULE_PATH%\views\price_change_views.xml
echo ^<odoo^> >> %MODULE_PATH%\views\price_change_views.xml
echo     ^<record id="view_price_change_form" model="ir.ui.view"^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="name"^>price.change.form^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="model"^>price.change^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="arch" type="xml"^> >> %MODULE_PATH%\views\price_change_views.xml
echo             ^<form^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<header^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^<field name="state" widget="statusbar" statusbar_visible="draft,pending,approved"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^</header^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<sheet^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^<div class="oe_title"^> >> %MODULE_PATH%\views\price_change_views.xml
echo                         ^<h1^> >> %MODULE_PATH%\views\price_change_views.xml
echo                             ^<field name="name"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                         ^</h1^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^</div^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^<group^> >> %MODULE_PATH%\views\price_change_views.xml
echo                         ^<group^> >> %MODULE_PATH%\views\price_change_views.xml
echo                             ^<field name="date"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                             ^<field name="change_type"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                             ^<field name="change_value"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                         ^</group^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^</group^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^<notebook^> >> %MODULE_PATH%\views\price_change_views.xml
echo                         ^<page string="Products"^> >> %MODULE_PATH%\views\price_change_views.xml
echo                             ^<field name="product_ids"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                         ^</page^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^</notebook^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^</sheet^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<div class="oe_chatter"^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^<field name="message_follower_ids"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^<field name="activity_ids"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                     ^<field name="message_ids"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^</div^> >> %MODULE_PATH%\views\price_change_views.xml
echo             ^</form^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo     ^</record^> >> %MODULE_PATH%\views\price_change_views.xml
echo. >> %MODULE_PATH%\views\price_change_views.xml
echo     ^<record id="view_price_change_tree" model="ir.ui.view"^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="name"^>price.change.tree^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="model"^>price.change^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="arch" type="xml"^> >> %MODULE_PATH%\views\price_change_views.xml
echo             ^<tree^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<field name="name"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<field name="date"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<field name="change_type"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<field name="change_value"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo                 ^<field name="state"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo             ^</tree^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo     ^</record^> >> %MODULE_PATH%\views\price_change_views.xml
echo. >> %MODULE_PATH%\views\price_change_views.xml
echo     ^<record id="action_price_change" model="ir.actions.act_window"^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="name"^>Price Changes^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="res_model"^>price.change^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo         ^<field name="view_mode"^>tree,form^</field^> >> %MODULE_PATH%\views\price_change_views.xml
echo     ^</record^> >> %MODULE_PATH%\views\price_change_views.xml
echo. >> %MODULE_PATH%\views\price_change_views.xml
echo     ^<menuitem id="menu_price_change" name="Price Changes" action="action_price_change" parent="sale.sale_menu_root" sequence="20"/^> >> %MODULE_PATH%\views\price_change_views.xml
echo ^</odoo^> >> %MODULE_PATH%\views\price_change_views.xml

echo Module created successfully! Place the %MODULE_PATH% folder in your Odoo addons directory.
pause