from odoo import models, fields, api

class VREquipment(models.Model):
    # Special Model Attributes
    _name = 'vr.equipment'
    _description = 'Virtual Reality Equipment'
    _order = 'purchase_date desc'

    # Simple Fields with Common Attributes
    name = fields.Char(string='Equipment Name', required=True, help='e.g., HTC VIVE Focus 3')
    
    brand = fields.Selection([
        ('htc', 'HTC'),
        ('meta', 'Meta'),
        ('valve', 'Valve')
    ], string='Brand', default='htc', required=True)
    
    is_available = fields.Boolean(string='Available for Loan', default=True)
    
    purchase_date = fields.Date(string='Purchase Date', default=fields.Date.context_today)
    
    notes = fields.Text(string='Technical Notes')
    
    serial_number = fields.Char(string='Serial Number', copy=False)

    # Ejemplo de un método ORM (Para entender self.env y recordsets)
    def action_mark_maintenance(self):
        # self en este punto es un Recordset
        for record in self:
            record.write({
                'is_available': False,
                'notes': f"Sent to maintenance on {fields.Date.today()}"
            })