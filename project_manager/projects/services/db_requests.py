from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404


from datetime import datetime
from projects.models import *



class TaskService:
    @classmethod
    def get_user_task_by_id(cls, user: User, id: int) -> Task:
        try:
            task = Task.objects.get(id=id, user=user)
            return task
        except Task.DoesNotExist:
            raise Http404('Такой задачи не существует')
    
    
    @classmethod
    def get_user_tasks(cls, user: User) -> QuerySet:
        return Task.objects.filter(user=user).order_by('-updated_at')

    