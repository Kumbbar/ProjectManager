from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View

from .services.db_requests import TaskService


class TaskFormView(View):
    form_template: str = None
    redirect_view: str = None
    custom_redirect: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.task = None
        self.form = None
        self.kwargs = {}

    def get_form(self, task_id: int):
        raise NotImplementedError

    def fill_form(self):
        pass

    def get(self, request: WSGIRequest, task_id: int, **kwargs):
        self.kwargs = kwargs
        self.view_preprocess(task_id)

        self.view_postprocess()
        return render(request, self.form_template, self.context)

    def post(self, request: WSGIRequest, task_id: int, **kwargs):
        self.kwargs = kwargs
        self.view_preprocess(task_id)

        if self.form.is_valid():
            self.form.save()

            self.view_postprocess()

            if self.custom_redirect:
                return self.redirect_view
            return redirect(self.redirect_view, task_id)
        self.view_postprocess()
        return render(request, self.form_template, self.context)

    def view_preprocess(self, task_id):
        self.task = TaskService.get_user_task_by_id(self.request.user, task_id)
        self.form = self.get_form(task_id)
        self.context.update({'task': self.task, 'form': self.form})

    def view_postprocess(self):
        pass


class DeleteView(View):
    redirect_view: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None

    def delete(self, **kwargs):
        self.kwargs = kwargs
        self.delete_object()
        return redirect('')

    def delete_object(self):
        raise NotImplementedError

