from django.contrib import admin

from .models import Task, TaskEvent, TaskStatus, ProjectStatus, Project, TaskFileStorage, ProjectFileStorage, \
 ProjectDocumentationNote


class BaseAdmin(admin.ModelAdmin):
    search_fields = ['name']


class TaskAdmin(BaseAdmin):
    list_display = ['name', 'user', 'project', 'created_at', 'updated_at', 'percentage_of_completion', 'task_status']


class TaskEventAdmin(BaseAdmin):
    list_display = ['name', 'task', 'created_at', 'updated_at']


class ProjectAdmin(BaseAdmin):
    list_display = ['name', 'created_at', 'director', 'project_status']


class ProjectDocumentationNoteAdmin(BaseAdmin):
    list_display = ['name', 'project', 'created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)
admin.site.register(Project, ProjectAdmin)

admin.site.register(TaskEvent, TaskEventAdmin)
admin.site.register(ProjectDocumentationNote, ProjectDocumentationNoteAdmin)

admin.site.register(ProjectStatus)
admin.site.register(TaskStatus)

admin.site.register(TaskFileStorage)
admin.site.register(ProjectFileStorage)
