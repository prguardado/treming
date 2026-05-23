from odoo import models, fields, api

class TremingInternActivities(models.Model):
    _name = 'treming.intern.activities'
    _description = 'Modelo Treming Intern Activities'
    
    intern_id = fields.Many2one('treming.intern', string='Pasante')
    date = fields.Date(string='Fecha', default=fields.Date.today())
    description = fields.Text(string='Descripción')
    difficulty = fields.Selection([
        ('easy', 'Leve'),
        ('medium', 'Media'),
        ('hard', 'Complicada')
    ], string='Dificultad', default='easy')
    product_id = fields.Many2one('product.product', string='Servicio')
    