from django.contrib import admin
from django.urls import path, include

from . import views
from .api import urls as api_urls
app_name = 'projects'

urlpatterns = [
    path('', views.get_tasks_page, name='get_tasks_page'),
    path('tasks/<int:task_id>', views.get_task_page, name='get_task_page'),
    path('tasks/<int:task_id>/update', views.UpdateTask.as_view(), name='update_task'),

    path('tasks/<int:task_id>/events/create', views.CreateTaskEvent.as_view(), name='create_event'),
    path('tasks/<int:task_id>/events/update/<int:event_id>', views.UpdateTaskEvent.as_view(), name='update_event'),

    path('tasks/<int:task_id>/files/create', views.CreateTaskFile.as_view(), name='create_task_file'),

    path('api/', include(api_urls)),

]

admin.site.index_title = "Управление задачами"

