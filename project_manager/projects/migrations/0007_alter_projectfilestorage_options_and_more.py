# Generated by Django 4.1.1 on 2023-04-15 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_remove_projectdocumentationnote_documentation_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectfilestorage',
            options={'verbose_name': 'Файл проекта', 'verbose_name_plural': 'Файлы проектов'},
        ),
        migrations.AlterModelOptions(
            name='taskfilestorage',
            options={'verbose_name': 'Файл задачи', 'verbose_name_plural': 'Файлы задач'},
        ),
    ]