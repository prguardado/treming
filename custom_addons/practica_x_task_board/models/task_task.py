from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class TaskTask(models.Model):
    _name = "x_task_board.task"
    _description = "Tarea"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, start_datetime asc, id desc"

    name = fields.Char(string="Título", required=True, tracking=True)
    active = fields.Boolean(default=True)
    description = fields.Html(string="Descripción")

    stage_id = fields.Many2one(
        "x_task_board.stage",
        string="Etapa",
        tracking=True,
        group_expand="_read_group_stage_ids",
        ondelete="restrict",
    )

    user_id = fields.Many2one(
        "res.users",
        string="Responsable",
        tracking=True,
        default=lambda self: self.env.user,
    )

    partner_id = fields.Many2one("res.partner", string="Cliente/Contacto")
    priority = fields.Selection(
        [
            ("0", "Baja"),
            ("1", "Media"),
            ("2", "Alta"),
            ("3", "Muy alta"),
        ],
        default="1",
        string="Prioridad",
        tracking=True,
    )

    kanban_state = fields.Selection(
        [
            ("normal", "En progreso"),
            ("blocked", "Bloqueada"),
            ("done", "Lista"),
        ],
        default="normal",
        string="Estado Kanban",
        tracking=True,
    )

    color = fields.Integer(string="Color")

    start_datetime = fields.Datetime(string="Inicio", tracking=True)
    end_datetime = fields.Datetime(string="Fin", tracking=True)
    is_all_day = fields.Boolean(string="Todo el día")

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("open", "En curso"),
            ("done", "Hecha"),
            ("cancel", "Cancelada"),
        ],
        default="draft",
        string="Estado",
        tracking=True,
    )

    # Recurrencia
    recurrence_enabled = fields.Boolean(string="Recurrente")
    recurrence_interval = fields.Integer(string="Cada", default=1)
    recurrence_unit = fields.Selection(
        [
            ("day", "Días"),
            ("week", "Semanas"),
            ("month", "Meses"),
        ],
        default="week",
        string="Unidad",
    )

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env["x_task_board.stage"].search([], order="sequence, id")

    def action_start(self):
        for rec in self:
            rec.state = "open"

    def action_done(self):
        for rec in self:
            rec.state = "done"
            if rec.recurrence_enabled:
                rec._create_next_recurrence()

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    def _create_next_recurrence(self):
        self.ensure_one()
        if not self.start_datetime:
            return

        delta = relativedelta()
        if self.recurrence_unit == "day":
            delta = relativedelta(days=self.recurrence_interval)
        elif self.recurrence_unit == "week":
            delta = relativedelta(weeks=self.recurrence_interval)
        elif self.recurrence_unit == "month":
            delta = relativedelta(months=self.recurrence_interval)

        new_start = self.start_datetime + delta
        new_end = self.end_datetime + delta if self.end_datetime else False

        self.copy({
            "state": "draft",
            "stage_id": self.env["x_task_board.stage"].search([], order="sequence, id", limit=1).id,
            "start_datetime": new_start,
            "end_datetime": new_end,
        })
