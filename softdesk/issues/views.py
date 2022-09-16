from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer,\
    IssueListSerializer, IssueDetailSerializer, CommentSerializer, ContributorSerializer  # UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .permissions import ProjectPermission, IssuePermission, CommentPermission, ContributorPermission


User = get_user_model()


class ProjectViewset(generics.ListCreateAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        projects = [
            contributors.project.id
            for contributors in Contributor.objects.filter(user=self.request.user)
        ]
        return Project.objects.filter(id__in=projects)

    def perform_create(self, serializer):
        """
        Add actions to execute during registration of the instance:
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
    permission_classes = [permissions.IsAuthenticated, ProjectPermission]

    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)


    def update(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectListSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewset(generics.ListCreateAPIView):
    serializer_class = IssueListSerializer
    permission_classes = [permissions.IsAuthenticated, IssuePermission]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_id'])

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
    permission_classes = [permissions.IsAuthenticated, IssuePermission]

    def retrieve(self):
        issue_id=self.kwargs['pk']
        issue = Issue.objects.all(id=issue_id)
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Issue.objects.all()
        issue = get_object_or_404(queryset, pk=pk)
        serializer = IssueListSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Issue.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewset(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermission]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_id'])

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the request.user as the author
        """
        comment = serializer.save(author=self.request.user)


class CommentDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermission]


class ContributorViewset(generics.ListCreateAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, ContributorPermission]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_id'])


class ContributorDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, ContributorPermission]
