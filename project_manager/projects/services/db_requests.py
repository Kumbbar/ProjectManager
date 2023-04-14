from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404

from ..models import Task, TaskEvent, TaskFileStorage


class TaskService:
    @classmethod
    def get_user_task_by_id(cls, user: User, task_id: int) -> Task:
        try:
            task = Task.objects.get(id=task_id, user=user)
            return task
        except Task.DoesNotExist:
            raise Http404('Такой задачи не существует')
    
    @classmethod
    def get_user_tasks(cls, user: User) -> QuerySet:
        return Task.objects.filter(user=user).order_by('-updated_at')


class TaskEventService:
    @classmethod
    def get_user_task_event_by_id(cls, user: User, event_id: int) -> Task:
        try:
            event = TaskEvent.objects.select_related('task').get(id=event_id, task__user=user)
            return event
        except TaskEvent.DoesNotExist:
            raise Http404('Такого события не существует')

    @classmethod
    def get_user_tasks(cls, user: User) -> QuerySet:
        return Task.objects.filter(user=user).order_by('-updated_at')


class TaskFileService:
    @classmethod
    def get_by_id(cls, file_id: int):
        return TaskFileStorage.objects.get(id=file_id)

    