from django.core.management.base import BaseCommand
from ...models import TaskStatusConsts, ProjectStatusConsts, TaskStatus, ProjectStatus


consts_and_models = (
    (TaskStatusConsts, TaskStatus),
    (ProjectStatusConsts, ProjectStatus),
)


class Command(BaseCommand):
    @staticmethod
    def is_status_exists(orm_model, status):
        return True if orm_model.objects.filter(name=status).first() else False

    def create_statuses_by_consts_model(self, status_consts, orm_model):
        for status in [a for a in dir(status_consts) if not a.startswith('__')]:
            if self.is_status_exists(orm_model, status):
                self.stdout.write(f'Status {status} already exists')
                continue
            new_status = orm_model(name=status)
            new_status.save()
            self.stdout.write(f'Status {status} created')

    def handle(self, *args, **options):
        for status_consts, orm_model in consts_and_models:
            self.create_statuses_by_consts_model(status_consts, orm_model)
        self.stdout.write(self.style.SUCCESS('Successfully ended'))