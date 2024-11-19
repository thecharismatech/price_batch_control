{ 
    'name': 'Price Management', 
    'version': '18.0.1.0.0', 
    'category': 'Sales', 
    'summary': 'Manage product price changes', 
    'author': 'Mahmoud Osama - Maxmatech', 
    'website': 'http://www.maxmatech.com', 
    'license': 'LGPL-3', 
    'depends': ['base', 'sale_management', 'purchase', 'mail'], 
    'data': [ 
        'security/ir.model.access.csv', 
        'data/price_change_sequence.xml', 
        'views/price_change_views.xml', 
    ], 
    'installable': True, 
    'application': True, 
    'auto_install': False, 
} 

