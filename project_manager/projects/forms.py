from django.forms import ModelForm
from django import forms
from django.db import models

from .models import Task, TaskStatus, TaskStatusConsts, TaskFileStorage, TaskEvent


class TaskFormUser(ModelForm):
    description = models.TextField(
        max_length=1500
    )
    percentage_of_completion = forms.IntegerField(
        label='Процент выполенения', 
        widget=forms.NumberInput(attrs={'class': 'form-control text', 'min': 0, 'max': 100})
    
    )
    task_status = forms.ModelChoiceField(
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control text'}),
        queryset=TaskStatus.objects.order_by('-id').exclude(name=TaskStatusConsts.CLOSED)
    )
    
    class Meta:
        model = Task
        labels = {
            'description': 'Описание'
        }
        fields = ['description', 'percentage_of_completion', 'task_status']


class TaskFormDirector(TaskFormUser):
    name = forms.CharField(
        label='Название',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control text'}),
        )
    task_status = forms.ModelChoiceField(
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control text'}),
        queryset=TaskStatus.objects.order_by('-id')
    )
    completion_date = forms.DateField(
        label='Срок завершения', 
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control text',
                'type': 'date'
            }
        ),
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'percentage_of_completion', 'task_status', 'completion_date']


class TaskEventForm(forms.ModelForm):
    name = forms.CharField(
        label='Название',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control text'}),
    )
    description = models.TextField(
        max_length=1500
    )

    class Meta:
        model = TaskEvent
        fields = ('name', 'description')


class TaskFileForm(forms.ModelForm):
    file = forms.FileField(
        label='Файл',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control text',
            }
        )
    )

    class Meta:
        model = TaskFileStorage
        fields = ('file',)
