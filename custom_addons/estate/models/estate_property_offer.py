from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    
    # Definición de atributos especiales para modelo
    _name = 'estate.property.offer'
    _description = 'Modelo para aplicación de ofertas a propiedades'
    
    # Se añade un atributo especial para el ordenamiento de registros mediante precios en forma descendente
    _order = 'price desc'
    
    # Definición de atributos comúnes de la clase EstatePropertyOffer
    price = fields.Float(string='Precio', help='Precio de la oferta')
    status = fields.Selection([
        ('accepted','Aceptado'),
        ('refused','Rechazado'),
    ], copy=False, string='Estado', help='Selección de estado de oferta')
    
    # Definición de atributos relacionales Many2one -----------------------------------------------------------------------------
    
    partner_id = fields.Many2one('res.partner', required=True, string='Asociado')
    property_id = fields.Many2one('estate.property', required=True, string='Propiedad')
    
    # --------------------------------------------------------------------------------------------------------------------------
    
    # Definición de campos para cálculo de validación de fechas en estate.property.offer
    
    # Se añade el campo validity para número de días de validez de la oferta
    validity = fields.Integer(string='Validez (días)', default=7, help='Número de días de validez de la oferta')
    
    # Se añade el campo calculado date_deadline
    date_deadline = fields.Date(string='Fecha de límite', compute='_compute_date_deadline', inverse='_inverse_date_deadline', help='Fecha de vencimiento de la oferta')
    
    
    # Definición de SQL Constraints --------------------------------------------------------------------------------------------
    
    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'El precio de la oferta debe ser positivo mayor a 0',
    )
    
    '''
    Forma restricciones SQL en versiones anteriores
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'El precio de la oferta debe ser positivo mayor a 0')
    ]
    '''
    
    # --------------------------------------------------------------------------------------------------------------------------
    
    
    # Definición de método para el campo calculado date_deadline ---------------------------------------------------------------
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            # Fallback: Si existe create_date, extraemos solo la fecha. Si no, se utiliza hoy
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            # Se suman los días de validez a la fecha base
            offer.date_deadline = base_date + timedelta(days=offer.validity)
            
    # Definición de método _inverse para el campo calculado date_deadline
    def _inverse_date_deadline(self):
        for offer in self:
            # Nuevamente un Fallback: si existe create_date, se extrae sólo la fecha. Si no se utiliza la fecha de hoy
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            # Ahora, se restan las fechas y se extrae el número de días
            offer.validity = (offer.date_deadline - base_date).days
    
    # Definición de métodos para estado de oferta -------------------------------------------------------------------------------
    
    # Definición de estado aceptado
    def action_accept_offer(self):
        for record in self:
            # Regla general: No aceptar algo ya rechazado
            if record.status == 'refused':
                raise UserError('Una oferta rechazada no puede ser aceptada.')
            
            # Nueva regla: validar que no esista ya otra oferta aceptada
            ofertas_aceptadas = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if ofertas_aceptadas:
                raise UserError('Esta propiedad ya tiene una oferta aceptada. No puedes aceptar más de una.')
            
            # Se cambia el estado de la oferta actual a aceptado
            record.status = 'accepted'
            
            # Asignar comprador y precio de venta al registro de propiedad
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            
            # Actualizar el estado de la propiedad como Oferta Recibida
            if record.property_id.state != 'offer_received':
                record.property_id.state = 'offer_received'
            
        # Al retornar True..
        return True
    
    # Definición de estado rechazado
    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('Una oferta aceptada no puede ser rechazada.')
            record.status = 'refused'
        return True