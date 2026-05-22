{
    'name': 'VR Lab Management',
    'version': '1.0',
    'summary': 'Módulo para gestión de laboratorio de realidad virtual',
    'category': 'Inventory',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/equipment_views.xml',
    ],
    'installable': True,
    'application': True,
}