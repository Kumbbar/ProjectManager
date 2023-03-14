from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest
from django.views import View

from .base_views import TaskFormView
from .services.db_requests import TaskService
from .services.forms import FormTaskService
from .filters import *
from .forms import TaskFileForm, TaskEventForm


@login_required
def get_tasks_page(request: WSGIRequest):
    tasks = TaskService.get_user_tasks(request.user)
    return render(request, 'projects/tasks.html', {'tasks': tasks})


@login_required
def get_task_page(request: WSGIRequest, task_id:int):
    task = TaskService.get_user_task_by_id(request.user, task_id)
    events = task.get_task_events()
    files = task.get_task_files()
    return render(request, 'projects/task.html', {
        'task': task, 
        'events': events,
        'files': files
        })


@method_decorator(login_required, name='dispatch')
class UpdateTask(TaskFormView):
    form_template = 'projects/task_update.html'
    redirect_view = 'projects:get_task_page'

    @staticmethod
    def get_task_and_form(request: WSGIRequest, task_id: int):
        task = TaskService.get_user_task_by_id(request.user, task_id)
        form = FormTaskService.get_task_form_by_user_position(task, request.user)(instance=task)
        if request.method == 'POST':
            form = FormTaskService.get_task_form_by_user_position(task, request.user)(data=request.POST,instance=task)
        return task, form

    def view_process(self):
        file_forms = FormTaskService.get_file_forms_for_task(self.task)
        self.context.update({'file_forms': file_forms})


@method_decorator(login_required, name='dispatch')
class CreateTaskEvent(TaskFormView):
    @staticmethod
    def get_task_and_form(request: WSGIRequest, task_id: int):
        task = TaskService.get_user_task_by_id(request.user, task_id)
        form = TaskEventForm()
        form.task = task
        return task, form

    def get(self, request: WSGIRequest, task_id: int):
        task, form = self.get_task_and_form(request, task_id)
        return render(request, 'projects/task_update.html', {'task': task, 'form': form})

    def post(self, request: WSGIRequest, task_id: int):
        task, form = self.get_task_and_form(request, task_id)
        if form.is_valid():
            form.save()
            return redirect('projects:get_task_page', task_id)
        file_forms = FormTaskService.get_file_forms_for_task(task)
        return render(request, 'projects/task_update.html', {'task': task, 'form': form, 'file_forms': file_forms})


@method_decorator(login_required, name='dispatch')
class UpdateTaskFile(View):            
    def post(self, request: WSGIRequest, task_id: int):
        form = TaskFileForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects:get_task_page', task_id)
        file_forms = get_file_forms_for_task(task)
        return render(request, 'projects/task_update.html', {'task': task, 'form': form, 'file_forms': file_forms})

