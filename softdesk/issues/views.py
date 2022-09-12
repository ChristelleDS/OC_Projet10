from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer,\
    IssueListSerializer, IssueDetailSerializer, CommentSerializer, ContributorSerializer  # UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly


User = get_user_model()


class ProjectViewset(generics.ListCreateAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        projects = [
            contributors.project.id
            for contributors in Contributor.objects.filter(user=self.request.user)
        ]
        return Project.objects.filter(id__in=projects)
        # return Project.objects.filter()

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the author
        - create the author as a contributor
        """
        project = serializer.save(author=self.request.user)
        contributor = Contributor.objects.create(
            user=project.author,
            project=project,
            permission='all',
            role='AUTH'
        )


class ProjectDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class IssueViewset(generics.ListCreateAPIView):
    serializer_class = IssueListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Issue.objects.filter()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the request.user as the author and default assignee
        """
        issue = serializer.save(author=self.request.user,
                                assignee=self.request.user)


class IssueDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class CommentViewset(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the request.user as the author
        """
        comment = serializer.save(author=self.request.user)


class CommentDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class ContributorViewset(generics.ListCreateAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self): # A CORRIGER
        queryset = Contributor.objects.all()
        project = self.request.query_params.get('project_id')
        if project is not None:
            queryset = queryset.filter(project=project)
        return queryset


class ContributorDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

"""
class UserViewset(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
"""