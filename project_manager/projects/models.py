from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet

import os
from dataclasses import dataclass
from datetime import datetime, date

from .validators import check_file_size
from project_manager.settings import MEDIA_URL, MEDIA_ROOT


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
    name = models.CharField(max_length=200, null=False, verbose_name='Название')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')

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

    def delete(self, using=None, keep_parents=False):
        os.remove(MEDIA_ROOT + self.file.name)
        return super(BaseFileStorage, self).delete(using, keep_parents)


# MODELS
class TaskStatus(BaseDescription):
    class Meta:
        db_table = 'task_statuses'
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'


class ProjectStatus(BaseDescription):
    class Meta:
        db_table = 'project_statuses'
        verbose_name = 'Статус проекта'
        verbose_name_plural = 'Статусы проектов'


class Project(BaseDescription):
    name = models.CharField(max_length=200, null=False, unique=True, verbose_name='Название')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    director = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='director',
        verbose_name='Руководитель'
    )
    users = models.ManyToManyField(User, verbose_name='Пользователи')
    project_status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Статус проекта'
    )

    class Meta:
        db_table = 'projects'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_project_events(self) -> QuerySet:
        return ProjectDocumentationNote.objects.filter(project=self).order_by('-created_at')

    def get_project_files(self) -> QuerySet:
        return ProjectFileStorage.objects.filter(project=self)


class ProjectDocumentationNote(BaseDescription):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        db_table = 'project_notes'
        verbose_name = 'Запись проекта'
        verbose_name_plural = 'Записи проектов'


class Task(BaseDescription):
    description = models.TextField(max_length=1500, null=True, blank=True, verbose_name='Описание')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Исполнитель')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='Проект')
    created_at = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    closed_at = models.DateTimeField(null=True, blank=True, editable=True, verbose_name='Завершено')
    percentage_of_completion = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Процент выполнения'
    )
    task_status = models.ForeignKey(
        TaskStatus,
        on_delete=models.SET_NULL,
        null=True, related_name='task_status',
        verbose_name='Статус')
    completion_date = models.DateField(null=True, blank=True, verbose_name='Срок выполнения')  # task deadline

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def close_task(self) -> None:
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

    def is_have_maximum_files(self) -> bool:
        return True if len(self.get_task_files()) >= 5 else False


class TaskEvent(BaseDescription):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, verbose_name='Задача')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        db_table = 'task_events'
        verbose_name = 'Событие задачи'
        verbose_name_plural = 'События задач'


# FILE MODELS
class ProjectFileStorage(BaseFileStorage):
    path = 'projects/%Y/%m/%d/'
    file = models.FileField(upload_to=path, **BaseFileStorage.base_params, verbose_name='Файл')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='Проект')

    class Meta:
        db_table = 'project_files'
        verbose_name = 'Файл проекта'
        verbose_name_plural = 'Файлы проектов'


class TaskFileStorage(BaseFileStorage):
    path = 'tasks/%Y/%m/%d/'
    file = models.FileField(upload_to=path, **BaseFileStorage.base_params, verbose_name='Файл')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, verbose_name='Задача')

    class Meta:
        db_table = 'task_files'
        verbose_name = 'Файл задачи'
        verbose_name_plural = 'Файлы задач'