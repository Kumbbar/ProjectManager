from django.contrib import admin
from django.urls import path, include

from . import views


app_name = 'projects'

urlpatterns = [
    path('', views.Tasks.as_view(), name='tasks'),
    path('tasks/<int:task_id>', views.TaskPage.as_view(), name='task'),
    path('tasks/<int:task_id>/update', views.UpdateTask.as_view(), name='update_task'),

    path('tasks/<int:task_id>/events/create', views.CreateTaskEvent.as_view(), name='create_event'),
    path('tasks/<int:task_id>/events/update/<int:event_id>', views.UpdateTaskEvent.as_view(), name='update_event'),
    path('tasks/<int:task_id>/events/delete/<int:event_id>', views.DeleteTaskEvent.as_view(), name='delete_event'),

    path('tasks/<int:task_id>/files/create', views.CreateTaskFile.as_view(), name='create_task_file'),
    path('tasks/<int:task_id>/files/delete/<int:file_id>', views.DeleteTaskFile.as_view(), name='delete_task_file'),

    path('projects/', views.Projects.as_view(), name='projects'),
    path('projects/<int:project_id>', views.ProjectPage.as_view(), name='project'),
]

admin.site.index_title = "Управление задачами"

