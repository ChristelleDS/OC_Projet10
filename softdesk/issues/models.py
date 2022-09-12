from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class Project(models.Model):

    TYPE_CHOICES = [
        ('Backend', 'Back'),
        ('Frontend', 'Front'),
        ('iOS', 'iOS'),
        ('Android', 'And'),
    ]

    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=500)
    type = models.CharField(choices=TYPE_CHOICES, max_length=8)
    author = models.ForeignKey('auth.User', related_name='projects', on_delete=models.CASCADE, blank=True)


class Contributor(models.Model):

    ROLE_CHOICES = [
        ('RESP', 'Responsable'),
        ('AUTH', 'Auteur'),
        ('CRE', 'Créateur'),
    ]

    PERM_LIST = [
        ("restricted", "Contributeur"),
        ("all", "Auteur"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(max_length=50, choices=PERM_LIST, default='restricted')
    role = models.fields.CharField(choices=ROLE_CHOICES, max_length=12, default="")

    class Meta:
        unique_together = ('user', 'project')


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

    title = models.fields.CharField(max_length=128)
    desc = models.fields.CharField(max_length=700, blank=True)
    tag = models.fields.CharField(choices=Tag.choices, max_length=12)
    priority = models.fields.CharField(max_length=20, choices=PRIORITY, default='L')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.fields.CharField(max_length=20, choices=STATUS, default='OP')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee', blank=True)
    created_time = models.fields.DateTimeField(default=timezone.now)


class Comment(models.Model):
    description = models.fields.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.fields.DateTimeField(default=timezone.now)
