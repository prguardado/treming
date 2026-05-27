from odoo import models, Command

# Definición de modelo para herecnia del modelo estate_property del módulo estate
class EstateProperty(models.Model):
    # Se hereda el modelo exacto que se requiere modificar
    _inherit = 'estate.property'
    
    # Adicionalmente, se sobreescribe el método que se ejecuta al hacer clic en "Vendida"
    # Para la creación de una factura se necesita: partner_id (el cliente), move_type (se tienen varios valores posibles), journal_id (la revista de contabilidad)
    def action_set_sold_property(self):
        # Impresión de un mensaje en terminal a modo de prueba
        # print("Módulo estate_acount ejecutando acción de venta")
        
        # Llamamos al método original usando super() para que realice su trabajo normal (Cambiar el estado, etc.).
        res = super().action_set_sold_property()
        
        # Se realiza una iteración sobre self, por si el usuario está procesando varias propiedades a la vez
        for record in self:
            # 3. Creamos la factura vacía usando self.env
            self.env['account.move'].create({
                # Pasamos el ID del comprador
                'partner_id' : record.buyer_id.id,
                # 'out_invoice' es el valor interno en Odoo para 'Customer Invoice' Factura Cliente
                'move_type': 'out_invoice',
                
                'invoice_line_ids': [
                    # Línea 1: 6% del precio de venta
                    Command.create({
                       'name': 'Comisión de venta (6%)',
                       'quantity': 1.0,
                       'price_unit': record.selling_price * 0.06,
                    }),
                    # Línea 2: Tarifa administrativa fija
                    Command.create({
                        'name': 'Tarifas administrativas',
                        'quantity': 1.0,
                        'price_unit': 100.00,
                    })
                ]
            })
        # Se retorna el resultado original
        return res
    
    
    