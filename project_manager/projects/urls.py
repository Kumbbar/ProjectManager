from django.urls import path
from django.conf.urls.static import static

from . import views
from project_manager import settings

app_name = 'projects'

urlpatterns = [
    path('', views.get_tasks_page, name='get_tasks_page'),
    path('tasks/<int:task_id>', views.get_task_page, name='get_task_page'),
    path('tasks/update/<int:task_id>', views.UpdateTask.as_view(), name='update_task'),
]

