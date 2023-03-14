from django.contrib.auth.models import User
from django.db.models import QuerySet

from typing import List, Tuple, Callable
from ..forms import TaskFormUser, TaskFormDirector, TaskFileForm
from ..models import Task, Project


class FormTaskService:
    def get_task_form_by_user_position(task: Task, user: User) -> Callable:
        if Project.objects.get(id=task.project.id).director == user:
            return TaskFormDirector
        return TaskFormUser

    def get_file_forms_for_task(task: Task) -> List[TaskFileForm]:
        files = task.get_task_files()
        forms = []
        for file in files:
            form = TaskFileForm(instance=file)
            form.filename = file.get_filename()
            forms.append(form)
        print(forms)
        return forms


class FormTaskFileService:
    def get_task_form_by_user_position(task: Task, user: User) -> Tuple[TaskFormUser, TaskFormDirector]:
        if Project.objects.get(id=task.project.id).director == user:
            return TaskFormDirector
        return TaskFormUser