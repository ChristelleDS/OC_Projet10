from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth import get_user_model


User = get_user_model()


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment_id', 'description', 'author_user_id', 'issue_id', 'created_time']


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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
