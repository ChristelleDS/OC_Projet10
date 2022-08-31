from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Project(models.Model):
    project_id = models.fields.IntegerField()
    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=500)
    type = models.fields.CharField(max_length=30)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.SET(get_sentinel_user))

    def save(self, *args, **kwargs):
        if self.author_user_id is None:
            self.author_user_id = User.id
        super().save(*args, **kwargs)


class Contributor(models.Model):

    class Role(models.Choices):
        Author = 0
        Responsible = 1
        Creator = 2

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    permission = models.fields.CharField(max_length=20)
    role = models.fields.CharField(choices=Role.choices,max_length=12)


class Issue(models.Model):

    class Tag(models.Choices):
        Bug = 0
        Task = 1
        Improvement = 2

    issue_id = models.fields.IntegerField()
    title = models.fields.CharField(max_length=128)
    desc = models.fields.CharField(max_length=700, blank=True)
    tag = models.fields.CharField(choices=Tag.choices, max_length=12)
    priority = models.fields.CharField(max_length=20)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.fields.CharField(max_length=20)
    author_user_id = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.fields.DateTimeField(default=timezone.now)


class Comment(models.Model):
    comment_id = models.fields.IntegerField()
    description = models.fields.CharField(max_length=500)
    author_user_id = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.fields.DateTimeField(default=timezone.now)
