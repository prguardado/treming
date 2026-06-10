{
    'name': 'Práctica Business Processes 1',
    'summary': 'Módulo de práctica para sistema de aprobación de gastos',
    'description': 'Módulo de práctica para sistema de aprobación de gastos',
    'version': '19.0.1.0.0',
    'author': 'Odoo-Dev',
    'website': 'www.test.com',
    'license': 'LGPL-3',
    'category': 'Test',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/expense_request_views.xml',
        'views/expense_request_menus_views.xml',
    ],
    'installable': True,
    'application': True,
}
