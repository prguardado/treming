from odoo import fields, model, api

class ResPartner(model.Model):
    # Definición de herencia del modelo res.partner
    _inherit = "res.partner"
    # Definición de campo a añadir al modelo res.partner para luego mostrar en la vista
    x_credit_score = fields.Integer(string="Credit Score", default="0")
    
    '''
    De este modo, no se crea un nuevo modelo en la bd, sino se añade un campo al modelo existente mediante
    _inherit. Siendo el patrón estándar para la extensión de modelos en Odoo
    
    Adicionalmente, el prefijo x_ es común para campos personalizados.
    '''