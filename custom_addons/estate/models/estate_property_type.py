from odoo import models, fields, api

class EstatePropertyType(models.Model):
    
    # Definición de atributos especiales del modelo
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type Model'
    
    # Se añade un atributo especial para el ordenamiento de los registros por nombre
    _order = 'sequence, name'
    
    # Definición de SQL Constraints --------------------------------------------------------------------------------------------
    
    _check_type_name = models.Constraint(
        'UNIQUE(name)',
        'El nombre del tipo de propiedad debe ser único.'
    )
    
    # -------------------------------------------------------------------------------------------------------------------------
    
    # Definición de campos con atributos comúnes para el modelo estate_property_type
    name = fields.Char(string='Nombre', required=True)
    
    # Ejercicio 11. List order Manual
    sequence = fields.Integer(string='Secuencia', default=1, help='Se utiliza para ordenar propiedades')
    
    # Definición de campo reservado activos
    active = fields.Boolean(string='Activo', default=True)
    
    # Definición de campos relacionales ---------------------------------------------------------------------------------------
    
    # Definición de atributo One2many property_ids
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Propiedades')
    
    # Ejercicio Capítulo  11 Parte final: Campos relacionales y calculados para offer_ids y offer_count
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Ofertas')
    offer_count = fields.Integer(string='Conteo de ofertas', compute='_compute_offer_count')
    
    # Método calculado para contar las ofertas
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            # len() cuenta cuántos registros hay dentro de offer_ids
            record.offer_count = len(record.offer_ids)