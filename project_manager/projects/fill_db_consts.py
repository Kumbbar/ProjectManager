import os, sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent.resolve())
import django

django.setup()

from models import TaskStatusConsts, ProjectStatusConsts, TaskStatus, ProjectStatus

if __name__ == '__main__':
    for status in TaskStatus:
        new_status = TaskStatus(name=status)
        new_status.save()

    for status in ProjectStatus:
        new_status = ProjectStatus(name=status)
        new_status.save()