from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View


class TaskFormView(View):
    form_template: str = None
    redirect_view: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.task = None
        self.form = None

    def get_task_and_form(self, task_id: int):
        task, form = None, None
        raise NotImplementedError

    def fill_form(self, form):
        raise NotImplementedError

    def get(self, request: WSGIRequest, task_id: int):
        self.task, self.form = self.get_task_and_form(task_id)
        self.context.update({'task': self.task, 'form': self.form})
        self.view_postprocess()
        return render(request, self.form_template, self.context)

    def post(self, request: WSGIRequest, task_id: int):
        self.task, self.form = self.get_task_and_form(task_id)
        self.context.update({'task': self.task, 'form': self.form})
        if self.form.is_valid():
            self.form.save()
            return redirect(self.redirect_view, task_id)
        self.view_postprocess()
        return render(request, self.form_template, self.context)

    def view_postprocess(self):
        pass
