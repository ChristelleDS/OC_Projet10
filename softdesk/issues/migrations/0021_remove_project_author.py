# Generated by Django 4.1 on 2022-09-09 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0020_alter_project_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='author',
        ),
    ]