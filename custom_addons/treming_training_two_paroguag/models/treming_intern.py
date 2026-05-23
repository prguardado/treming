from odoo import models, fields, api
from odoo.exceptions import UserError

class TremingIntern(models.Model):
    _name = 'treming.intern'
    _description = 'Módulo Treming Intern'
    
    name = fields.Char(string='Nombre', required=True)
    birth_date = fields.Date(string='Fecha de Nacimiento')
    gender = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino')
    ], string='Género', default='male')
    country_id = fields.Many2one('res.country', string='País')
    email = fields.Char(string='Correo electrónico')
    university_id = fields.Many2one('res.partner', string='Universidad')
    career = fields.Char(string='Carrera')
    hobbies = fields.Html(string='Pasatiempos')
    category_ids = fields.Many2many('res.partner.category', string='Categorías')
    referred = fields.Boolean(string='referido', default=False)
    
    activity_ids = fields.One2many('treming.intern.activities', 'intern_id', string='Actividades de Pasante')
    