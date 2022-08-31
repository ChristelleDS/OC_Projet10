from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Project, Contributor, Issue, Comment



class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'description', 'author_user_id', 'issue_id', 'created_time']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'project_id', 'status',
                  'author_user_id', 'assignee_user_id', 'created_time']

    def validate_title(self, value):
        if Issue.objects.filter(title=value).exists():
            raise ValidationError('Issue already exists')
        return value


class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'project_id', 'status',
                  'author_user_id', 'assignee_user_id', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = instance.comment.filter()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise ValidationError('Project already exists')
        return value


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id', 'contributors', 'issues']

    def get_contributors(self, instance):
        queryset = instance.contributor.filter()
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data

    def get_issues(self, instance):
        queryset = instance.issue.filter()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


