# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Test',
    # 'sequence': 15, # El campo 'sequence' en el archivo __manifest__.py de un módulo de Odoo se utiliza para determinar el orden en el que se muestran los módulos en la lista de aplicaciones dentro del sistema. Un número más bajo en el campo 'sequence' hará que el módulo aparezca antes en la lista, mientras que un número más alto hará que aparezca después. Esto es útil para organizar los módulos de manera lógica y facilitar a los usuarios encontrar y acceder a los módulos que necesitan. En este caso, el valor '15' indica que este módulo de CRM se mostrará después de los módulos con una secuencia menor a 15 y antes de los módulos con una secuencia mayor a 15.
    'summary': 'Este es un ejemplo de módulo de prueba para el sector inmobiliario.',
    'description': ''' Este es un módulo de prueba para el sector inmobiliario que se utiliza para demostrar cómo crear un módulo personalizado en Odoo. Este módulo incluye funcionalidades básicas para gestionar propiedades, clientes, agentes inmobiliarios y contratos de alquiler. El objetivo de este módulo es proporcionar una base sólida para que los desarrolladores puedan construir sobre ella y agregar funcionalidades adicionales según las necesidades específicas de su negocio inmobiliario. ''',
    'website': 'https://www.realestate.com',
    'depends': [
        'base',
    ],
    'data': [
        # Este apartado de security sirve para definir las reglas de acceso y los permisos de los usuarios en el módulo. Esto incluye la definición de grupos de usuarios, las reglas de acceso a los modelos y las vistas, y cualquier otra configuración relacionada con la seguridad del módulo. Es importante configurar correctamente la seguridad para garantizar que los usuarios tengan acceso solo a la información y funcionalidades que les corresponden según su rol en la organización.
        #'security/crm_security.xml',
        'security/ir.model.access.csv',

        # Este apartado de views sirve para definir las vistas del módulo, como por ejemplo las vistas de formulario, las vistas de lista, las vistas de calendario, etc. Estas vistas son necesarias para que los usuarios puedan interactuar con el módulo y acceder a la información y funcionalidades que ofrece. Las vistas también pueden incluir acciones, botones y otros elementos de interfaz de usuario para facilitar la navegación y el uso del módulo.
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus_views.xml',        

        # Este apartado de data sirve para cargar datos de configuración, como por ejemplo los tipos de actividad del módulo, las etapas de oportunidad, los motivos de pérdida, etc. Estos datos son necesarios para que el módulo funcione correctamente y estén disponibles para los usuarios desde el momento en que se instala el módulo.
        # 'data/crm_lead_merge_template.xml',
        # 'data/crm_lead_prediction_data.xml',

        # Este apartado de views sirve para definir las vistas del módulo, como por ejemplo las vistas de formulario, las vistas de lista, las vistas de calendario, etc. Estas vistas son necesarias para que los usuarios puedan interactuar con el módulo y acceder a la información y funcionalidades que ofrece. Las vistas también pueden incluir acciones, botones y otros elementos de interfaz de usuario para facilitar la navegación y el uso del módulo.
        
        # El bundle para los wizards se llama 'wizard' y se utiliza para agrupar las vistas relacionadas con los asistentes o wizards del módulo. Los wizards son interfaces de usuario que guían a los usuarios a través de un proceso específico, como la creación de una oportunidad a partir de un lead, la fusión de oportunidades, la actualización masiva de leads, etc. Al agrupar estas vistas en un bundle llamado 'wizard', se facilita la organización y el mantenimiento del código relacionado con los asistentes del módulo.
        # 'wizard/crm_lead_lost_views.xml',
        
    ],
    # El apartado de demo sirve para cargar datos de demostración en el módulo. Estos datos son útiles para mostrar cómo funciona el módulo y para que los usuarios puedan probar sus funcionalidades con datos reales. Los datos de demostración pueden incluir ejemplos de clientes, oportunidades, actividades, equipos de ventas, etc. Estos datos no son necesarios para el funcionamiento del módulo, pero pueden ser muy útiles para que los usuarios comprendan mejor cómo utilizar el módulo y para que puedan probar sus funcionalidades antes de usarlo con datos reales.
    'demo': [
        # 'data/crm_team_demo.xml',
    ],
    'installable': True,    # El campo 'installable' en el archivo __manifest__.py de un módulo de Odoo se utiliza para indicar si el módulo puede ser instalado en el sistema. Si el valor es 'True', el módulo estará disponible para su instalación a través de la interfaz de usuario de Odoo. Si el valor es 'False', el módulo no estará disponible para su instalación y no podrá ser utilizado en el sistema. Esto es útil para controlar qué módulos están disponibles para los usuarios y para evitar que se instalen módulos que aún están en desarrollo o que no son compatibles con la versión actual de Odoo.
    'application': True,    # El campo 'application' en el archivo __manifest__.py de un módulo de Odoo se utiliza para indicar si el módulo es una aplicación principal o no. Si el valor es 'True', el módulo se considerará una aplicación principal y aparecerá en la lista de aplicaciones dentro del sistema. Si el valor es 'False', el módulo se considerará un módulo complementario o de soporte y no aparecerá en la lista de aplicaciones, aunque aún podrá ser instalado y utilizado en el sistema. Esto es útil para organizar los módulos y facilitar a los usuarios encontrar las aplicaciones principales que necesitan.
    
    # El apartado de assets se utiliza para definir los recursos estáticos que el módulo necesita para funcionar correctamente. Esto incluye archivos CSS, JavaScript, imágenes, etc. Estos recursos se agrupan en bundles específicos, como 'web.assets_backend' para los recursos utilizados en la interfaz de administración, 'web.assets_backend_lazy' para los recursos que se cargan de forma diferida, 'web.assets_tests' para los recursos utilizados en las pruebas, etc. Al definir estos assets en el archivo __manifest__.py, Odoo puede gestionar y cargar estos recursos de manera eficiente cuando el módulo se instala y se utiliza.
    'assets': {

        # El bundle 'web.assets_backend' se utiliza para definir los recursos estáticos que se cargarán en la interfaz de administración de Odoo. En este caso, se incluyen todos los archivos dentro de 'crm/static/src/**', pero se excluyen específicamente los archivos dentro de 'crm/static/src/views/forecast_graph/**' y 'crm/static/src/views/forecast_pivot/**'. Esto significa que estos últimos archivos no se cargarán en la interfaz de administración, lo que puede ser útil para optimizar el rendimiento o para evitar conflictos con otros módulos.
        'web.assets_backend': [
            # 'crm/static/src/**',
            # ('remove', 'crm/static/src/views/forecast_graph/**'),
            # ('remove', 'crm/static/src/views/forecast_pivot/**'),
        ],
        # El bundle 'web.assets_backend_lazy' se utiliza para definir los recursos estáticos que se cargarán de forma diferida en la interfaz de administración de Odoo. En este caso, se incluyen específicamente los archivos dentro de 'crm/static/src/views/forecast_graph/**' y 'crm/static/src/views/forecast_pivot/**'. Esto significa que estos archivos se cargarán solo cuando sea necesario, lo que puede ayudar a mejorar el rendimiento de la interfaz de administración al no cargar estos recursos de inmediato.
        'web.assets_backend_lazy': [
            # 'crm/static/src/views/forecast_graph/**',
            # 'crm/static/src/views/forecast_pivot/**',
        ],
        # El bundle 'web.assets_tests' se utiliza para definir los recursos estáticos que se cargarán durante la ejecución de las pruebas en Odoo. En este caso, se incluyen todos los archivos dentro de 'crm/static/tests/tours/**', lo que significa que estos recursos estarán disponibles durante las pruebas para simular la interacción del usuario con la interfaz de Odoo y verificar que el módulo funcione correctamente.
        'web.assets_tests': [
            #'crm/static/tests/tours/**/*',
        ],
        # El bundle 'web.assets_unit_tests' se utiliza para definir los recursos estáticos que se cargarán durante la ejecución de las pruebas unitarias en Odoo. En este caso, se incluyen todos los archivos dentro de 'crm/static/tests/mock_server/**/*' y el archivo 'crm/static/tests/crm_test_helpers.js'. Esto significa que estos recursos estarán disponibles durante las pruebas unitarias para simular un servidor de prueba y proporcionar funciones de ayuda específicas para las pruebas del módulo CRM.
        'web.assets_unit_tests': [
            'crm/static/tests/mock_server/**/*',
            'crm/static/tests/crm_test_helpers.js'
        ],
        # El bundle 'web.qunit_suite_tests' se utiliza para definir los recursos estáticos que se cargarán durante la ejecución de las pruebas QUnit en Odoo. En este caso, se incluyen todos los archivos dentro de 'crm/static/tests/**/*', pero se excluyen específicamente los archivos dentro de 'crm/static/tests/tours/**', 'crm/static/tests/mock_server/**' y el archivo 'crm/static/tests/crm_test_helpers.js'. Esto significa que estos últimos recursos no se cargarán durante las pruebas QUnit, lo que puede ser útil para evitar conflictos o para optimizar el rendimiento de las pruebas.
        'web.qunit_suite_tests': [
            # Se incluyen todos los archivos dentro de 'crm/static/tests/**/*'
            #'crm/static/tests/**/*',
            # Se excluyen los siguientes recursos de las pruebas QUnit
            #('remove', 'crm/static/tests/tours/**/*'),
        ],
    },
    'author': 'RealEstate Inc.',
    'license': 'LGPL-3',
}