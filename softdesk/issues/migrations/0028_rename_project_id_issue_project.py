# Generated by Django 4.1 on 2022-09-12 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0027_rename_issue_id_comment_issue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='project_id',
            new_name='project',
        ),
    ]