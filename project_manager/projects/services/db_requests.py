from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


from ..models import Task, TaskEvent, TaskFileStorage, Project


class BaseService:
    @staticmethod
    def not_exist_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except ObjectDoesNotExist:
                raise Http404('Такой страницы не существует')
        return wrapper


# TASKS SERVICES


class TaskService(BaseService):
    @classmethod
    @BaseService.not_exist_decorator
    def get_user_task_by_id(cls, user: User, task_id: int) -> Task:
            task = Task.objects.get(id=task_id, user=user)
            return task

    @classmethod
    def get_user_tasks(cls, user: User) -> QuerySet:
        return Task.objects.filter(user=user).order_by('-updated_at')


class TaskEventService(BaseService):
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


class TaskFileService(BaseService):
    @classmethod
    def get_by_id(cls, file_id: int):
        return TaskFileStorage.objects.get(id=file_id)


# PROJECTS SERVICES


class ProjectService(BaseService):
    @classmethod
    def get_by_updated_time(cls):
        projects = Project.objects.order_by('-updated_at')
        return projects

    @classmethod
    def get_by_id(cls, project_id):
        return Project.objects.get(id=project_id)
