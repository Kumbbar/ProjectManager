from django.contrib.auth.models import User

from typing import Callable
from ..forms import TaskFormUser, TaskFormDirector
from ..models import Task, Project


class FormTaskService:
    @staticmethod
    def get_task_form_by_user_position(task: Task, user: User) -> Callable:
        if Project.objects.get(id=task.project.id).director == user:
            return TaskFormDirector
        return TaskFormUser
