from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Project(models.Model):

    TYPE_CHOICES = [
        ('Back', 'Backend'),
        ('Front', 'Frontend'),
        ('iOS', 'iOS'),
        ('And', 'Android'),
    ]

    project_id = models.fields.IntegerField()
    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=500)
    type = models.CharField(choices=TYPE_CHOICES, max_length=7)
    author_user_id =  models.ManyToManyField('Contributor', related_name='projects')

    def save(self, *args, **kwargs):
        if self.author_user_id is None:
            self.author_user_id = User.id
        super().save(*args, **kwargs)


class Contributor(models.Model):

    ROLE_CHOICES = [
        ('RES', 'Responsable'),
        ('AUT', 'Auteur'),
        ('CON', 'Contributeur'),
    ]

    PERM_LIST = [
        ("restricted", "Contributeur"),
        ("all", "Auteur"),
    ]


    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(max_length=50, choices=PERM_LIST, default='restricted')
    role = models.fields.CharField(choices=ROLE_CHOICES,max_length=12, default="")


class Issue(models.Model):

    class Tag(models.Choices):
        Bug = 0
        Task = 1
        Improvement = 2

    PRIORITY = [('L', 'Low'),
                ('M', 'Medium'),
                ('H', 'High')
                ]

    STATUS = [('OP', 'OPEN'),
        ('IP', 'IN PROGRESS'),
        ('CL', 'Closed')
        ]

    issue_id = models.fields.IntegerField()
    title = models.fields.CharField(max_length=128)
    desc = models.fields.CharField(max_length=700, blank=True)
    tag = models.fields.CharField(choices=Tag.choices, max_length=12)
    priority = models.fields.CharField(max_length=20, choices=PRIORITY, default='L')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.fields.CharField(max_length=20, choices=STATUS, default='Ouvert')
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignee')
    created_time = models.fields.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.author_user_id is None:
            self.author_user_id = User.id
        if self.assignee_user_id is None:
            self.assignee_user_id = User.id
        super().save(*args, **kwargs)

class Comment(models.Model):
    comment_id = models.fields.IntegerField()
    description = models.fields.CharField(max_length=500)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.fields.DateTimeField(default=timezone.now)
