Here's a comprehensive breakdown of the price_batch_control module:

Files Structure:

price_batch_control/
├── __init__.py
├── __manifest__.py
├── models/
│   └── product.py
├── security/
│   ├── ir.model.access.csv
│   └── price_control_security.xml
├── views/
│   ├── actions.xml
│   ├── menu_views.xml
│   ├── price_change_log_views.xml
│   ├── product_views.xml
│   ├── purchase_order_views.xml
│   └── stock_picking_views.xml
└── wizards/
    ├── __init__.py
    ├── price_change_wizard.py
    └── price_change_wizard_views.xml

Copy

Apply

Models:

ProductTemplate (inherits product.template):

Fields:
price_change_count (Integer, computed)
price_change_ids (One2many)
Methods:
_compute_price_change_count()
_search_display_name()
action_view_price_changes()
PriceChangeWizard (TransientModel):

Fields:
source (Selection)
source_document_id (Reference)
change_type (Selection)
change_value (Float)
product_ids (Many2many)
effective_date (Date)
company_id (Many2one)
Methods:
_onchange_source()
action_apply_changes()
Views:

Product Views:

Extended product form view with price changes
Price changes list view
Smart button for price history
Purchase Order Views:

Extended purchase order form with price change button
Context-aware wizard launch
Stock Picking Views:

Extended stock transfer form with price updates
Wizard Views:

Price change wizard form
Selection fields for change type
Product multi-selection
Action buttons
Menu Items:

Price Control main menu
Price Changes submenu
Reports menu
Security:

Access rights for models
Record rules for multi-company
User groups definitions
Dependencies:

base
product
sale_management
purchase
stock
account
This module follows Odoo 18 standards with:

Modern chatter implementation
List view instead of tree view
New access control methods
Updated translation system
Modern SQL operations