from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    # Special Model Attributes como _name, _description, _order, etc. se utilizan para definir características específicas del modelo. Por ejemplo, _name define el nombre técnico del modelo que se utilizará en la base de datos y en el código, mientras que _description proporciona una descripción legible para los usuarios sobre el propósito del modelo. Estos atributos son importantes para organizar y estructurar el modelo de manera clara y eficiente dentro del sistema Odoo.
    _name = 'estate.property'
    _description = 'Real Estate Property'
    
    # Añadir un campo para el ordenamiento de los ID en forma descensdente
    _order = 'id desc'

    # Definición de función para calcular la fecha 3 meses después de la fecha actual
    def _default_date_availability(self):
        return fields.Date.context_today(self) + timedelta(days=90)
    
    # Apartado de campos simples con atributos comunes ------------------------------------------------------------------------

    # el atributo name no podrá ser nulo
    name = fields.Char(string='Nombre de la propiedad', required=True, help='e.g., Apartamento en el centro de la ciudad')
    description = fields.Text(string='Descripción', help='Descripción detallada de la propiedad, incluyendo características, ubicación, etc.')
    postcode = fields.Char(string='Código postal', help='e.g., 28001')
    # El campo 'date_availability' es un campo de tipo Date que se utiliza para indicar la fecha a partir de la cual una propiedad estará disponible para su alquiler o venta. Este campo es importante para gestionar el inventario de propiedades y para informar a los clientes sobre cuándo podrán acceder a la propiedad. Al establecer una fecha de disponibilidad, los agentes inmobiliarios pueden planificar mejor las visitas y las negociaciones con los clientes interesados en la propiedad.
    date_availability = fields.Date(string='Disponible desde', default=_default_date_availability, copy=False, help='Fecha de disponibilidad de la propiedad')
    expected_price = fields.Float(string='Precio Esperado', required=True, help='El precio que el propietario espera obtener por la propiedad.')
    selling_price = fields.Float(string='Precio de Venta', readonly=True, copy=False, help='El precio al que se vendió la propiedad. Este campo es de solo lectura porque se calcula automáticamente cuando se confirma la venta de la propiedad.')
    bedrooms = fields.Integer(string='Número de habitaciones', default=2, help= 'El número de habitaciones en la propiedad. Esto es importante para los clientes que buscan propiedades con un número específico de habitaciones para satisfacer sus necesidades de espacio y comodidad.')
    
    # Definición de campo calculado total_area
    total_area = fields.Integer(string='Área Total (m²)', compute="_compute_total_area")
    
    living_area = fields.Integer(string='Área habitable (m²)', default=60, help='El área habitable de la propiedad en metros cuadrados')
    facades = fields.Integer(string='Número de fachadas', default=2, help='El número de fachadas de la propiedad puede influir en la cantidad de luz natural que recibe, entre otros factores')
    garage = fields.Boolean(string='Garaje', default=False, help='Indica si la propidad tiene un garaje')
    garden = fields.Boolean(string='Jardín', default=False, help='Indica si la propiedad tiene un jardín. Un jardín puede ser un factor importante para muchos compradores, ya que proporciona un espacio al aire libre para actividades recreativas')
    garden_area = fields.Integer(string='Área del jardín (m²)', default=0, help='El área del jardín en metros cuadrados')
    garden_orientation = fields.Selection([
        ('north', 'Norte'),
        ('south', 'Sur'),
        ('east', 'Este'),
        ('west', 'Oeste')
    ], string='Orientación del jardín', help='La orientación del jardín puede afectar la cantidad de luz solar que recibe, lo que a su vez puede influir en el crecimiento de las plantas y en la comodidad del espacio al aire libre. Por ejemplo, un jardín orientado al sur generalmente recibe más luz solar durante el día, lo que puede ser ideal para cultivar plantas que requieren mucha luz. Por otro lado, un jardín orientado al norte puede recibir menos luz directa, lo que podría ser más adecuado para plantas que prefieren sombra o para crear un espacio más fresco durante los meses de verano.')

    # Definición de campo reservado active
    active = fields.Boolean(string='Activo', default=True, help='Indica si la propiedad está activa o no')
    
    # Definición de campo Many2many para estate_property_tag
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetas', help='Etiquetas relacionadas con la propiedad')

    # Definición de campo reservado state
    state = fields.Selection([
        ('new', 'Nuevo'),
        ('offer_received', 'Oferta Recibida'),
        ('offer_accepted', 'Oferta Aceptada'),
        ('sold', 'Vendida'),
        ('canceled', 'Cancelada')
    ], string='Estado', default='new', required=True, copy=False, help='Estado actual de la propiedad')
    
    # Se añade el campo relacional Many2one para asignación de tipo de propiedad al modelo estate.property -----------------------
    
    property_type_id = fields.Many2one('estate.property.type', string='Tipo de propiedad', copy=False) 
    
    # Se añaden dos campos adicionales Many2one, siendo buyer y salesperson ------------------------------------------------------
   
    # buyer, puede ser cualquier individuo.
    buyer_id = fields.Many2one('res.partner', string='Comprador', copy=False)
   
    # Luego salesperson debe ser un empleado de Real Estte Agency
    salesperson_id = fields.Many2one('res.users', string='Vendedor', index=True, tracking=True, default=lambda self: self.env.user)
    
    # Definición de atributo offer_ids al modelo estate.property -----------------------------------------------------------------

    offer_ids = fields.One2many("estate.property.offer", "property_id", string='Ofertas')
    
    # Definición de campo calculado best_price ----------------------------------------------------------------------------------

    best_price = fields.Float(string='Mejor oferta', compute='_compute_best_price')
    
    # Definición de campo relacional property_type_id ---------------------------------------------------------------------------
    property_type_id = fields.Many2one('estate.property.type', string='Tipo de propiedad', copy=False)
    
    # Definición de restricciones SQL -------------------------------------------------------------------------------------------
    
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 
        'El precio esperado de venta debe ser positivo mayor a 0',
    )
    
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)', 
        'El precio de venta debe ser positivo',
    )
       
    # Definición de método de restricción python ----------------------------------------------------------------------
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_python(self):
        for record in self:
            # Ignorar si el precio de venta es cero (Tip de ejercicio)
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            
            # Calcular el 90% del precio esperado
            min_price = record.expected_price * 0.90
            
            # Comparar los decimales utilizando la herramienta de Odoo
            # float_compare devuelve -1 si el primer valor es menor que el segundo
            if float_compare(record.selling_price, min_price, precision_digits=2) == -1:
                raise ValidationError("El precio de venta no puede ser menor que el '90%' del precio esperado de venta.")
            
    # ------------------------------------------------------------------------------------------------------------------
            
    # Definición de método para campo calculado total_area = living_area + garden_area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    '''            
    # Definición de método para campo calculado best_price, es definido como el más alto de las ofertas (offers' price)
    # Forma alternativa
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))'''
    
    # Definición de método para campo calculado best_price
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            precios = record.offer_ids.mapped('price')
            if precios:
                record.best_price = max(precios)
            else:
                record.best_price = 0.0
                
    # Definición de método Onchange --------------------------------------------------------------------------------------------
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            # 
            self.garden_area = 0
            self.garden_orientation = ''
        
    # Definición de métodos para acciones --------------------------------------------------------------------------------------
    
    # Marcar propiedad como Vendida    
    def action_set_sold_property(self):
        for record in self:
            # Se valida si el estado es 'canceled', no se pueda asignar el estado 'sold'
            if record.state == 'canceled':
                raise UserError('Una propiedad cancelada no puede ser vendida.')
            # Si no, entonces se asigna el estado 'sold'
            record.state = 'sold'
        # Se indica que la acción finalizó exitosamente y refresca la pantalla
        return True
            
    # Marcar propiedad como cancelada    
    def action_set_cancelled_property(self):
        for record in self:
            # Se valida que la propiedad no esté marcada con el estado de 'sold'(vendida)
            if record.state == 'sold':
                raise UserError('Una propiedad vendida no puede ser cancelada.')
            record.state == 'canceled'
        return True
               
    # Capítulo 12: Ejercicio de herencia Python --------------------------------------------------------------------------------
    
    @api.ondelete(at_uninstall=False)    
    def _unlink_except_new_or_canceled(self):
        # Self puede contener múltiples registros si el usuario selecciona varios en la lista y presiona "Eliminar"
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError('Sólo se pueden eliminar propiedades que se encuentren en el estado Nuevo o Cancelado.')
    
    # --------------------------------------------------------------------------------------------------------------------------
    
    
    # Ejemplo de recordset para crear una propiedad
    @api.model # El decorador @api.model se utiliza para indicar que el método es un método de modelo, lo que significa que se puede llamar sin necesidad de una instancia específica del modelo. Esto es útil para crear registros o realizar operaciones que no dependen de un registro específico, como en este caso, donde se crea una nueva propiedad utilizando el método create.
    def create_sample_property(self):
        sample_property = self.create({
            'name': 'Apartamento en el centro de la ciudad',
            'description': 'Un hermoso apartamento de 2 habitaciones ubicado en el corazón de la ciudad, cerca de tiendas, restaruantes y transporte público.',
            'postcode': '28001',
            'date_availability': self._default_date_availability,
            'expected_price': 250000,
            'bedrooms': 2,
            'living_area': 80,
            'facades': 3,
            'garage': True,
            'garden': False,
            'garden_area': 0,
            'garden_orientation': 'south',
        })

    # Ejemplo de recordset para actualizar el precio de venta de una propiedad
    def sell_property(self, selling_price):
        # Como 'self' es un recordset, puede contener múltiples registros. Se ha de iterar sobre el conjunto de registros
        for record in self:
            record.write({'selling_price': selling_price})
        
    # Ejemplo de operaciones avanzadas con recordsets en Odoo
    @api.model
    def get_expensive_garages(self):
        # 1. Obtener un recordset desde la base de datos usando search()
        properties_with_garage = self.search([('garage', '=', True)])        
        # 2. Operaciones sobre el recordset: filtrado (filtered) y mapeo (mapped)
        expensive_properties = properties_with_garage.filtered(lambda p: p.expected_price > 200000)
        property_names = expensive_properties.mapped('name')        
        return property_names
