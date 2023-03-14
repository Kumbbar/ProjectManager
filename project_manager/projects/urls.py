from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.get_tasks_page, name='get_tasks_page'),
    path('tasks/<int:task_id>', views.get_task_page, name='get_task_page'),
    path('tasks/update/<int:task_id>', views.UpdateTask.as_view(), name='update_task'),
    # path('tasks/event/update/<int:task_id>', views.UpdateTask.as_view(), name='update_task'),
    # path('tasks/file/update/<int:file_id>', views.UpdateTaskFile.as_view(), name='update_task_file'),
    # path('tasks/create/<int:task_id>', views.UpdateTask.as_view(), name='update_task'),
    path('tasks/create_event/<int:task_id>', views.UpdateTask.as_view(), name='create_even'),


]

