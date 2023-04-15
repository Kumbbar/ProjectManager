from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View
from django.forms import ModelForm

from .services.db_requests import TaskService


class FilterView(View):
    template: str = None
    filter = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.query_set = {}

    def get(self, request: WSGIRequest) -> render:
        self.get_query_set()
        data_filter = self.filter(request.GET, queryset=self.query_set)
        return render(request, self.template, {'filter': data_filter})

    def get_query_set(self) -> None:
        raise NotImplementedError


class PageView(View):
    page_template: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.kwargs = {}
        self.object = {}
        self.object_events = []
        self.object_files = []

    def get(self, request: WSGIRequest, **kwargs) -> render:
        self.kwargs = kwargs
        self.get_object_data()
        context = {
            'object': self.object,
            'object_files': self.object_files,
            'object_events': self.object_events
        }
        return render(request, self.page_template, context)

    def get_object_data(self) -> None:
        raise NotImplementedError


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

    def get_form(self, task_id: int) -> (None, ModelForm):
        raise NotImplementedError

    def fill_form(self) -> (None, ModelForm):
        pass

    def get(self, request: WSGIRequest, task_id: int, **kwargs) -> render:
        self.kwargs = kwargs
        self.view_preprocess(task_id)

        self.view_postprocess()
        return render(request, self.form_template, self.context)

    def post(self, request: WSGIRequest, task_id: int, **kwargs) -> (render, redirect):
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

    def view_preprocess(self, task_id: int) -> None:
        self.task = TaskService.get_user_task_by_id(self.request.user, task_id)
        self.form = self.get_form(task_id)
        self.context.update({'task': self.task, 'form': self.form})

    def view_postprocess(self) -> None:
        pass


class DeleteView(View):
    return_data = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None

    def post(self, request: WSGIRequest, **kwargs) -> return_data:
        self.kwargs = kwargs
        self.delete_object()
        return self.return_data

    def delete_object(self) -> None:
        raise NotImplementedError
