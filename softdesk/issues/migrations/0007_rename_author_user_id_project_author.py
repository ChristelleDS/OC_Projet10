# Generated by Django 4.1 on 2022-09-05 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0006_remove_project_contrib_users_project_author_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='author_user_id',
            new_name='author',
        ),
    ]