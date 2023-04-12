from django import forms

from .models import Task, Project, TaskStatus
from django_filters import FilterSet, OrderingFilter, ModelChoiceFilter, CharFilter


class TaskFilter(FilterSet):

    name = CharFilter(
        label='Название',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Название задачи',
                'class': 'form-control text'
            }
        )
    )
    task_status = ModelChoiceFilter(
        queryset=TaskStatus.objects.all(),
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control text'}),
    )

    project = ModelChoiceFilter(
        queryset=Project.objects.all(),
        label='Проект',
        widget=forms.Select(attrs={'class': 'form-control text'}),
    )
    create_time_ordering = OrderingFilter(
        choices=(
            ('created_at', 'По возрастанию'),
            ('-created_at', 'По убыванию'),
        ),
        fields=(
            ('created_at', 'created_at'),
            ('-created_at', '-created_at'),
        ),
        label="Дата создания",
        widget=forms.Select
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
        label='Срок выполнения',
    )

    class Meta:
        model = Task
        fields = ['name', 'task_status', 'project', 'create_time_ordering', 'deadline_time_ordering']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        order_by_filter = self.form.fields["create_time_ordering"]
        order_by_filter.widget.attrs = {
            'class': 'form-control'
        }
        order_by_filter = self.form.fields["deadline_time_ordering"]
        order_by_filter.widget.attrs = {
            'class': 'form-control'
        }