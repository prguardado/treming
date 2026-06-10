from odoo import models, fields
from odoo.exceptions import ValidationError, UserError

class ExpenseRequest(models.Model):
    _name = 'expense.request'
    _description = 'Expense Request'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Importante para historial (tracking)
    
    name = fields.Char(string='Nombre', required=True, tracking=True)
    amount = fields.Float(string='Monto', required=True, tracking=True)
    
    # 1. Definición del campo estate, para cambio de estado
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('submitted', 'Enviado para Aprobación'),
        ('approved', 'Aprobado'),
        ('paid', 'Pagado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft', tracking=True, required=True)
    
    # 2. Definición de métodos para transición (Reglas de negocio)
    def action_submit(self):
        for request in self:
            if request.amount <= 0:
                raise ValidationError('El monto debe ser mayor a cero.')
            request.state = 'submitted'
            return True
    
    def action_approve(self):
        for request in self:
            # Acá se podría añadir lógica para verificar si el usuario es Gerente
            request.state = 'approved'
            return True
        
    def action_pay(self):
        for request in self:
            # Acá se podría generar el asiento contable
            request.state = 'paid'
            return True
        
    def action_cancel(self):
        for request in self:
            request.state = 'cancelled'
            return True
        
    def action_draft(self):
        for request in self:
            request.state = 'draft'
            return True
    
    # Asegurar el flujo a nivel de base de datos
    def write(self, vals):
        # Si intentan modificar campos críticos y no esta en borrador
        for request in self:
            if request.state not in ['draft'] and any(field in vals for field in ['name', 'amount']):
                raise UserError("No es posible modificar una solicitud de gasto que ya fue enviada o procesada.")
        return super(ExpenseRequest, self).write(vals)
    
    def unlink(self):
        # Impedir el borrado si no sta en borraodr o cancelado
        for request in self:
            if request.state not in ['draft', 'cancelled']:
                raise UserError("Solo puedes eliminar gastos en estado Borrador o Cancelado.")
        return super(ExpenseRequest, self).unlink()
