from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest

from .base_views import TaskFormView, DeleteView, FilterView, PageView
from .services.db_requests import TaskService, TaskEventService, TaskFileService, ProjectService
from .services.forms import FormTaskService
from .filters import *
from .data_filters import TaskFilter, ProjectFilter
from .forms import TaskFileForm, TaskEventForm


@method_decorator(login_required, name='dispatch')
class Tasks(FilterView):
    template = 'projects/tasks.html'
    filter = TaskFilter

    def get_query_set(self):
        self.list = TaskService.get_user_tasks(self.request.user)


@method_decorator(login_required, name='dispatch')
class Projects(FilterView):
    template = 'projects/projects.html'
    filter = ProjectFilter

    def get_query_set(self):
        self.list = ProjectService.get_by_updated_time()


@method_decorator(login_required, name='dispatch')
class TaskPage(PageView):
    page_template = 'projects/task.html'

    def get_object_data(self):
        self.object = TaskService.get_user_task_by_id(self.request.user, self.kwargs['task_id'])
        self.object_events = self.object.get_task_events()
        self.object_files = self.object.get_task_files()


@method_decorator(login_required, name='dispatch')
class ProjectPage(PageView):
    page_template = 'projects/project.html'

    def get_object_data(self):
        self.object = ProjectService.get_by_id(self.kwargs['project_id'])
        self.object_events = self.object.get_project_events()
        self.object_files = self.object.get_project_files()


@method_decorator(login_required, name='dispatch')
class UpdateTask(TaskFormView):
    form_template = 'projects/task_update.html'
    redirect_view = 'projects:task'

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


@method_decorator(login_required, name='dispatch')
class CreateTaskEvent(TaskFormView):
    form_template = 'projects/task_event_create.html'
    redirect_view = 'projects:task'

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
    redirect_view = 'projects:task'

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
    return_data = HttpResponse("Success")

    def delete_object(self):
        file = TaskFileService.get_by_id(self.kwargs['file_id'])
        file.delete()


@method_decorator(login_required, name='dispatch')
class DeleteTaskEvent(DeleteView):
    return_data = HttpResponse("Success")

    def delete_object(self):
        event = TaskEventService.get_user_task_event_by_id(self.request.user, self.kwargs['event_id'])
        event.delete()