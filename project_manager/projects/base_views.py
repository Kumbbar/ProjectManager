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

    @staticmethod
    def get_task_and_form(request: WSGIRequest, task_id: int):
        task, form = None, None
        raise NotImplementedError

    def get(self, request: WSGIRequest, task_id: int):
        self.task, self.form = self.get_task_and_form(request, task_id)
        self.context.update({'task': self.task, 'form': self.form})
        self.view_process()
        return render(request, self.form_template, self.context)

    def post(self, request: WSGIRequest, task_id: int):
        task, form = self.get_task_and_form(request, task_id)
        if form.is_valid():
            form.save()
            return redirect(self.redirect_view, task_id)
        self.view_process()
        return render(request, self.form_template, self.context)

    def view_process(self):
        pass
