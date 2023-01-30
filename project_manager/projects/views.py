from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest
from django.views import View

from .services.db_requests import TaskService
from .services.forms import get_task_form_by_user_position
from .filters import *
from .forms import TaskFormUser


@login_required
def get_tasks_page(request: WSGIRequest):
    tasks = TaskService.get_user_tasks(request.user)
    return render(request, 'projects/tasks.html', {'tasks': tasks})


@login_required
def get_task_page(request: WSGIRequest, task_id:int):
    task = TaskService.get_user_task_by_id(request.user, task_id)
    form = TaskFormUser(instance=task)
    events = task.get_task_events()
    return render(request, 'projects/task.html', {'task': task, 'events': events})


@method_decorator(login_required, name='dispatch')
class UpdateTask(View):
    def get(self, request: WSGIRequest, task_id: int):
        task = TaskService.get_user_task_by_id(request.user, task_id)
        form = get_task_form_by_user_position(task, request.user)(instance=task)
        events = task.get_task_events()
        return render(request, 'projects/task_update.html', {'task': task, 'form': form})
    
    def post(self, request: WSGIRequest, task_id: int):
        task = TaskService.get_user_task_by_id(request.user, task_id)
        form = get_task_form_by_user_position(task, request.user)(data=request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('projects:get_task_page', task_id)
        return render(request, 'projects/task_update.html', {'task': task, 'form': form})

