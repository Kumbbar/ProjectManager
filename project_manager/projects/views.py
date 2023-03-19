from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest
from django.views import View

from .base_views import TaskFormView
from .services.db_requests import TaskService, TaskEventService
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
    form_template = 'projects/task_form.html'
    redirect_view = 'projects:get_task_page'

    def fill_form(self, form):
        if self.request.method == 'POST':
            form = form(data=self.request.POST, instance=self.task)
        else:
            form = form(instance=self.task)
        self.form = form

    def get_form(self, task_id: int):
        self.form = FormTaskService.get_task_form_by_user_position(self.task, self.request.user)
        self.fill_form(self.form)
        return self.form

    def view_postprocess(self):
        file_forms = FormTaskService.get_file_forms_for_task(self.task)
        self.context.update({'file_forms': file_forms})


@method_decorator(login_required, name='dispatch')
class CreateTaskEvent(TaskFormView):
    form_template = 'projects/task_event_create.html'
    redirect_view = 'projects:get_task_page'

    def fill_form(self, form):
        self.form = form(data=self.request.POST)
        return self.form

    def get_form(self, task_id: int):
        self.form = TaskEventForm
        self.fill_form(self.form)
        self.form.instance.task_id = self.task.pk
        return self.form


@method_decorator(login_required, name='dispatch')
class UpdateTaskEvent(TaskFormView):
    form_template = 'projects/task_event_update.html'
    redirect_view = 'projects:get_task_page'

    def fill_form(self, form):
        event = TaskEventService.get_user_task_event_by_id(self.request.user, self.kwargs['event_id'])
        self.context['event'] = event

        if self.request.method == 'POST':
            form = form(data=self.request.POST, instance=event)
        else:
            form = form(instance=event)
        self.form = form

    def get_form(self, task_id: int):
        self.form = TaskEventForm
        self.fill_form(self.form)
        return self.form


# @method_decorator(login_required, name='dispatch')
# class UpdateTaskFile(View):
#     def post(self, request: WSGIRequest, task_id: int):
#         form = TaskFileForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('projects:get_task_page', task_id)
#         file_forms = get_file_forms_for_task(task)
#         return render(request, 'projects/task_update.html', {'task': task, 'form': form, 'file_forms': file_forms})

