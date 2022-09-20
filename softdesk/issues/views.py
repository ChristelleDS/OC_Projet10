from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer,\
    IssueListSerializer, IssueDetailSerializer, CommentSerializer, ContributorSerializer  # UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import viewsets
from .permissions import ProjectPermission, IssuePermission, CommentPermission, ContributorPermission
from rest_framework.decorators import api_view


User = get_user_model()


class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, viewsets.ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
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


class IssueViewset(MultipleSerializerMixin, viewsets.ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IssuePermission]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the request.user as the author and default assignee
        """
        issue = serializer.save(author=self.request.user,
                                assignee=self.request.user)

    def retrieve(self, request, project_pk=None, pk=None, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=pk)
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data)

    def update(self, request, project_pk=None, pk=None, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=pk)
        serializer = IssueListSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewset(MultipleSerializerMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    detail_serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermission]

    def get_queryset(self):
        return Comment.objects.filter(issue_id= self.request.kwargs['issue_pk'])

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the request.user as the author
        """
        comment = serializer.save(author=self.request.user)

    def retrieve(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewset(MultipleSerializerMixin, viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, ContributorPermission]

    def get_queryset(self, request, project_pk):
        contrib_ids = [contributor.user.id
                       for contributor
                       in Contributor.objects.filter(project_id=project_pk)]
        return User.objects.filter(id__in=contrib_ids)
