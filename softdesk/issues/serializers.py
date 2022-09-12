from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = "__all__"

    def validate_title(self, value):
        if Issue.objects.filter(title=value).exists():
            raise ValidationError('Issue already exists')
        return value


class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'project_id', 'status',
                  'author', 'assignee', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = instance.comment.filter()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields =  ['title','description','type','author']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError('Project already exists')
        return value


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors', 'issues']

    def get_contributors(self, instance):
        queryset = instance.contributor.filter()
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data

    def get_issues(self, instance):
        queryset = instance.issue.filter()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']
        # Make a new member active & staff by default, so it can do CRUD operations
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=True)
