{
    'name':'treming_training_two_paroguag',
    'version':'19.0.1.0.0',
    'category':'Test',
    'description':'''Realiación de módulo treming_training_two_paroguag para prueba técnica de entrenamiento''',
    'version': '1.0',
    'depends':[
        'base',
        'crm',
        'sale_management',
        'stock',
        'contacts',
    ],
    'data':[
        'security/ir.model.access.csv',
        'data/crm_team_data.xml',
        'data/product_attribute_data.xml',
        'data/res_partner_data.xml',
        'data/treming_intern_views.xml'
        
    ],
    'installable':True,
    'application':False,
    'author':'Patrick_Guardado',
    'license':'LGPL-3',
}