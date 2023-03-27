from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class TaskApi(View):
    http_method_names = ['delete']

    @csrf_exempt
    def delete(self, request: WSGIRequest):
        self.ss = 1488
        return JsonResponse({'sdasd': 'we2e'})

