/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { registry } from "@web/core/registry";

class TaskSwimlaneKanbanController extends KanbanController {
    static template = "x_task_board.TaskSwimlaneKanbanView";

    setup() {
        super.setup();
    }
}

export const taskSwimlaneKanbanView = {
    ...kanbanView,
    Controller: TaskSwimlaneKanbanController,
};

registry.category("views").add("x_task_swimlane_kanban", taskSwimlaneKanbanView);