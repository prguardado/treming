from odoo import models, fields, api

class ResUsers(models.Model):
    # _inherit le dice a Odoo "Busca ese modelo existente y agrégale lo que está abajo"
    _inherit = 'res.users'
    
    # Relación inversa: Un usuario puede ser vendedor de muchas propiedades
    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Propiedades', domain=[('state', 'in', ['new', 'offer_received'])])
    