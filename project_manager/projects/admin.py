from django.contrib import admin

from .models import Task, TaskEvent, TaskStatus, ProjectStatus, Project, TaskFileStorage


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'project', 'created_at', 'updated_at', 'percentage_of_completion', 'task_status']


class TaskEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'task', 'created_at', 'updated_at']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'director', 'project_status']


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskEvent, TaskEventAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStatus)
admin.site.register(TaskStatus)
admin.site.register(TaskFileStorage)
