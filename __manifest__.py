{
    'name': 'Price Batch Control',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Manage product price changes in batch from purchase orders',
    'author': 'Mahmoud Osama - Maxmatech',
    'website': 'http://www.maxmatech.com',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'purchase', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/price_batch_sequence.xml',
        'views/price_batch_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

