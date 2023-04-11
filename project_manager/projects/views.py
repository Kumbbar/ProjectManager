from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest

from .base_views import TaskFormView
from .services.db_requests import TaskService, TaskEventService
from .services.forms import FormTaskService
from .filters import *
from .data_filters import TaskFilter
from .forms import TaskFileForm, TaskEventForm


@login_required
def get_tasks_page(request: WSGIRequest):
    tasks = TaskService.get_user_tasks(request.user)
    task_filter = TaskFilter(request.GET, queryset=tasks)
    return render(request, 'projects/tasks.html', {'task_filter': task_filter})


@login_required
def get_task_page(request: WSGIRequest, task_id: int):
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

    def fill_form(self):
        if self.request.method == 'POST':
            self.form = self.form(data=self.request.POST, instance=self.task)
        else:
            self.form = self.form(instance=self.task)

    def get_form(self, task_id: int):
        self.form = FormTaskService.get_task_form_by_user_position(self.task, self.request.user)
        self.fill_form()
        return self.form


@method_decorator(login_required, name='dispatch')
class CreateTaskEvent(TaskFormView):
    form_template = 'projects/task_event_create.html'
    redirect_view = 'projects:get_task_page'

    def fill_form(self):
        self.form = self.form(data=self.request.POST)

    def get_form(self, task_id: int):
        self.form = TaskEventForm
        self.fill_form()
        self.form.instance.task_id = self.task.pk
        return self.form


@method_decorator(login_required, name='dispatch')
class UpdateTaskEvent(TaskFormView):
    form_template = 'projects/task_event_update.html'
    redirect_view = 'projects:get_task_page'

    def fill_form(self):
        event = TaskEventService.get_user_task_event_by_id(self.request.user, self.kwargs['event_id'])
        self.context['event'] = event

        if self.request.method == 'POST':
            self.form = self.form(data=self.request.POST, instance=event)
        else:
            self.form = self.form(instance=event)

    def get_form(self, task_id: int):
        self.form = TaskEventForm
        self.fill_form()
        return self.form


@method_decorator(login_required, name='dispatch')
class CreateTaskFile(TaskFormView):
    form_template = 'projects/add_file_form.html'
    redirect_view = 'projects:get_task_page'

    def view_postprocess(self):
        pass

    def fill_form(self):
        self.form = self.form(self.request.POST, self.request.FILES)

    def get_form(self, task_id: int):
        self.form = TaskFileForm
        self.fill_form()
        self.form.instance.task_id = self.task.pk
        return self.form
