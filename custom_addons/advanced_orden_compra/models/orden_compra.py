# -*- coding: utf-8 -*-
from odoo import models, fields, api

class OrdenCompraAvanzada(models.Model):
    _name = 'orden.compra.avanzada'
    _description = 'Orden de Compra Práctica'

    name = fields.Char(string='Referencia', required=True, default='Nueva')
    fecha = fields.Date(string='Fecha de Orden', default=fields.Date.context_today)
    proveedor_id = fields.Many2one('res.partner', string='Proveedor', required=True)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('urgente', 'Prioridad Urgente')
    ], string='Estado', default='borrador')
    linea_ids = fields.One2many('orden.compra.avanzada.line', 'orden_id', string='Líneas')

class OrdenCompraAvanzadaLine(models.Model):
    _name = 'orden.compra.avanzada.line'
    _description = 'Líneas de Orden de Compra Práctica'

    orden_id = fields.Many2one('orden.compra.avanzada', string='Orden Referencia', ondelete='cascade')
    producto = fields.Char(string='Producto/Servicio', required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)
    precio_unitario = fields.Float(string='Precio Unitario')
