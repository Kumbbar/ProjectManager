from .models import Task, Project, TaskStatus
from django_filters import FilterSet, OrderingFilter, ModelChoiceFilter, CharFilter


class TaskFilter(FilterSet):
    name = CharFilter(label='Название')
    task_status = ModelChoiceFilter(queryset=TaskStatus.objects.all(), label='Статус')
    project = ModelChoiceFilter(queryset=Project.objects.all(), label='Проект')
    create_time_ordering = OrderingFilter(
        choices=(
            ('created_at', 'По возрастанию'),
            ('-created_at', 'По убыванию'),
        ),
        fields=(
            ('created_at', 'created_at'),
            ('-created_at', '-created_at'),
        ),
        label="Дата создания"
    )
    deadline_time_ordering = OrderingFilter(
        choices=(
            ('completion_date', 'По возрастанию'),
            ('-completion_date', 'По убыванию'),
        ),
        fields=(
            ('completion_date', 'completion_date'),
            ('-completion_date', '-completion_date'),
        ),
        label='Срок выполнения'
    )

    class Meta:
        model = Task
        fields = ['name', 'task_status', 'project', 'create_time_ordering', 'deadline_time_ordering']