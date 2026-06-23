# -*- coding: utf-8 -*-
{
    'name': 'Orden de Compra Avanzada (Práctica QWeb)',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Módulo didáctico para dominar directivas QWeb en Odoo 19.0',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/orden_compra_views.xml',
        'reports/report_orden_compra_actions.xml',
        'reports/report_orden_compra_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}