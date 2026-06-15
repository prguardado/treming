from odoo import fields, models

class TaskStage(models.Model):
    _name = "x_task_board.stage"
    _description = "Etapa de tarea"
    _order = "sequence, id"

    name = fields.Char(string="Nombre", required=True)
    sequence = fields.Integer(string="Secuencia", default=10)
    fold = fields.Boolean(string="Plegada")
    color = fields.Integer(string="Color")