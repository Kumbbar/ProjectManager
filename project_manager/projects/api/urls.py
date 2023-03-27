from django.urls import path

from .views import TaskApi


urlpatterns = [
    path('task', TaskApi.as_view(), name='tesk_api')
]
