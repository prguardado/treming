{
    "name": "Task Board",
    "version": "19.0.1.0.0",
    "summary": "Tablero de tareas con vistas Kanban, Calendar y Activity",
    "description": "Tablero de tareas con vistas Kanban, Calendar y Activity",
    "website": "www.test.com",
    "category": "Productivity",
    "author": "Odoo-Dev",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/task_stage_data.xml",
        "views/task_stage_views.xml",
        "views/task_task_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "x_task_board/static/src/js/task_swimlane_kanban_controller.js",
            "x_task_board/static/src/xml/task_swimlane_kanban.xml",
        ],
    },
    "installable": True,
    "application": True,
}
