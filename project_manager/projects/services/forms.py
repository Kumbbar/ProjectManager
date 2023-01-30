from django.contrib.auth.models import User

from typing import Tuple
from projects.forms import TaskFormUser, TaskFormDirector
from projects.models import Task, Project


def get_task_form_by_user_position(task: Task, user: User) -> Tuple[TaskFormUser, TaskFormDirector]:
    if Project.objects.get(id=task.project.id).director == user:
        return TaskFormDirector
    return TaskFormUser