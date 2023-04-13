from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest

from .base_views import TaskFormView, DeleteView
from .services.db_requests import TaskService, TaskEventService, TaskFileService
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
    return render(
        request,
        'projects/task.html',
        {
            'task': task,
            'events': events,
            'files': files
        }
    )


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

    def view_postprocess(self):
        self.context['files'] = self.task.get_task_files()
        print(self.task.get_task_files())


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
    redirect_view = 'projects:create_task_file'
    custom_redirect = True

    def view_postprocess(self):
        if self.request.method == 'POST' and not self.form.errors:
            self.context.update({'success_add': True})
        self.redirect_view = render(self.request, self.form_template, self.context)

    def fill_form(self):
        self.form = self.form(self.request.POST, self.request.FILES)
        return self.form

    def get_form(self, task_id: int):
        self.form = TaskFileForm
        self.fill_form()
        self.form.instance.task_id = self.task.pk
        if self.task.is_have_maximum_files():
            self.form.errors['file'] = ErrorList(['Нельзя добавить больше 5 файлов'], )
        return self.form


@method_decorator(login_required, name='dispatch')
class DeleteTaskFile(DeleteView):
    redirect_view = 'projects:create_task_file'

    def delete_object(self):
        file = TaskFileService.get_by_id(self.kwargs['file_id'])
        file.delete()