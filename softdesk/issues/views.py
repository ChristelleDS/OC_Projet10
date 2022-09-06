from rest_framework import generics
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer, \
    IssueListSerializer, IssueDetailSerializer, CommentSerializer, ContributorSerializer


class ProjectViewset(generics.ListCreateAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return Project.objects.filter()


class ProjectDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class IssueViewset(generics.ListCreateAPIView):
    serializer_class = IssueListSerializer

    def get_queryset(self):
        queryset = Issue.objects.filter()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class IssueDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueDetailSerializer


class CommentViewset(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset


class CommentDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ContributorViewset(generics.ListCreateAPIView):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        queryset = Contributor.objects.filter()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class ContributorDetailViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

class UserViewset(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
