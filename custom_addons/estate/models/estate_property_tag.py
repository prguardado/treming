from odoo import models, fields, api

class EstatePrpertyTag(models.Model):
    
    # Definición de atributos especiales de modelo
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag Model'
    
    # Se añade un atributo especial para el ordenamiento de los registros por nombre 
    _order = 'name'
    
    # Definición de SQL Constaints -----------------------------------------------------------------------------------------
    
    _check_tag_name = models.Constraint(
        'UNIQUE(name)',
        'El nombre de la etiqueta debe ser único.'
    )
    
    # ---------------------------------------------------------------------------------------------------------------------
    
    # Definición de atributos comunes para el modelo estate_property_tag
    name = fields.Char(string='Nombre', required=True, copy=False)
    
    # Capítulo 11 Ejercicio widget options --------------------------------------------------------------------------------
    color = fields.Integer(string='Color Index')
    
    # Definición de atributo reservado Active de tipo Boolean
    active = fields.Boolean(string='Activo', default=True)
    
    
    
    