from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet

import os
from dataclasses import dataclass
from datetime import datetime, date

from .validators import check_file_size
from project_manager.settings import MEDIA_URL



# CONSTANTS

@dataclass
class TaskStatusConsts:
    NEW: str = "Новая"
    IN_PROGRESS: str = "В процессе"
    SOLVED: str = "Решена"
    CLOSED: str = "Закрыта"
    PENDING: str = "Ожидает"
    REJECTED: str = "Отклонена"

@dataclass
class ProjectStatusConsts:
    OPEN: str = "Открытый"
    CLOSED: str = "Закрытый"


# BASE MODELS
class BaseDescription(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.name}'


class BaseFileStorage(models.Model):
    path = '//'
    base_params = {
        'max_length': 100,
        'validators': [check_file_size]
    }
    
    file = models.FileField(upload_to=path)
    
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.file}'
    
    def get_filename(self) -> str:
        return os.path.basename(self.file.name)

    def get_absolute_url(self) -> str:
        return f'{MEDIA_URL}{self.file.name}'


# MODELS
class TaskStatus(BaseDescription):
    class Meta:
        db_table = 'task_statuses'
        verbose_name_plural = 'Task_statuses'


class ProjectStatus(BaseDescription):
    class Meta:
        db_table = 'project_statuses'
        verbose_name_plural = 'Project_statuses'


class Project(BaseDescription):
    name = models.CharField(max_length=200, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='director')
    users = models.ManyToManyField(User)
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'projects'

    def test(self):
        print(self.name)


class ProjectDocumentation(BaseDescription):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)


class DocumenationNote(BaseDescription):
    documentation = models.ForeignKey(ProjectDocumentation, on_delete=models.CASCADE)


class Task(BaseDescription):
    description = models.TextField(max_length=1500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True, editable=True)
    percentage_of_completion =  models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    task_status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True, related_name='task_status')
    completion_date = models.DateField(null=True, blank=True)  # task deadline

    class Meta:
        db_table = 'tasks'

    def close_task(self, datetime : datetime) -> None:
        self.closed_at = datetime.now()
        self.task_status = TaskStatus.objects.get(name=TaskStatusConsts.CLOSED)
        self.percentage_of_completion = 100
        self.save()
    
    def is_expired(self) -> bool:
        if isinstance(self.completion_date, datetime) and isinstance(self.completion_date, date):
            return self.closed_at > datetime.combine(self.completion_date, datetime.min.time())
        if isinstance(self.completion_date, date):
            return datetime.now() > datetime.combine(self.completion_date, datetime.min.time())
        return False
    
    def get_task_events(self) -> QuerySet:
        return TaskEvent.objects.filter(task=self).order_by('-created_at')
    
    def get_task_files(self) -> QuerySet:
        return TaskFileStorage.objects.filter(task=self)


class TaskEvent(BaseDescription):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task_events'


# FILE MODELS
class ProjectFileStorage(BaseFileStorage):
    path ='projects/%Y/%m/%d/'
    file = models.FileField(upload_to=path, **BaseFileStorage.base_params)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'project_files'


class TaskFileStorage(BaseFileStorage):
    path = 'tasks/%Y/%m/%d/'
    file = models.FileField(upload_to=path, **BaseFileStorage.base_params)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'task_files'


class TaskEventFileStorage(BaseFileStorage):
    path = 'task_events/%Y/%m/%d/'
    file = models.FileField(upload_to=path, **BaseFileStorage.base_params)
    task_event = models.ForeignKey(TaskEvent, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'task_event_files' 


class DocumenationNoteFileStorage(BaseFileStorage):
    path = 'documentation_notes/%Y/%m/%d/'
    file = models.FileField(upload_to=path, **BaseFileStorage.base_params)
    documenation_note = models.ForeignKey(DocumenationNote, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'documentation_files' 