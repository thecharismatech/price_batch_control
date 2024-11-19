{
    'name': 'Price Batch Control',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': 'Batch Price Control and History. Manage product prices in batch operations with full history tracking. - Batch price updates - Price change history - Approval workflow',
    'author': 'Mahmoud Osama',
    'website': 'https://maxmatech.com',
    'depends': ['base', 'product', 'sale_management', 'purchase', 'stock', 'account'],
    'data': [
        'security/price_control_security.xml',
        'security/ir.model.access.csv',
        'views/price_change_log_views.xml',
        'views/product_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'wizards/price_change_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}