from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer,\
    IssueListSerializer, IssueDetailSerializer, CommentSerializer, ContributorSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import viewsets
from .permissions import ProjectPermission, IssuePermission, CommentPermission, ContributorPermission



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
    permission_classes = [permissions.IsAuthenticated & ProjectPermission]

    def get_queryset(self):
        """
        :return: list of projects which the user is a contributor
        """
        projects = [
            contributors.project.id
            for contributors in Contributor.objects.filter(user_id=self.request.user.id)
        ]
        return Project.objects.filter(id__in=projects)

    def perform_create(self, serializer):
        """
        Add actions to execute during registration of the instance:
        - save the author
        - create the author as a contributor
        Any user can create a new project.
        """
        project = serializer.save(author=self.request.user)
        contributor = Contributor.objects.create(
            user=project.author,
            project=project,
            permission='all',
            role='AUTH'
        )

    def retrieve(self, request, pk=None):
        """
        Only a contributor of the project can read details about it.
        """
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, project)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Only the author of the project can update it.
        """
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(self.request, project)
        serializer = ProjectListSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Only the author of the project can delete it.
        """
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(self.request, project)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewset(MultipleSerializerMixin, viewsets.ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [permissions.IsAuthenticated & IssuePermission]

    def get_queryset(self):
        """
        Only a contributor of the project can get the list of issues.
        :return: list of issues for the project in param
        """
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.check_object_permissions(self.request, project)
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the request.user as the author and default assignee
        """
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.check_object_permissions(self.request, project)
        issue = serializer.save(author=self.request.user,
                                assignee=self.request.user)

    def retrieve(self, request, project_pk=None, pk=None, *args, **kwargs):
        """
        Check requested data:
        - if project and issue don't match: error "unknown data" is raised
        - if match : return detailed data if permissions ok
        """
        issue = get_object_or_404(Issue, pk=pk)
        project = get_object_or_404(Project, pk=project_pk)
        if issue.project.id == project.id:
            self.check_object_permissions(self.request, project)
            serializer = IssueDetailSerializer(issue)
            return Response(serializer.data)
        else:
            return Response('Unknown data requested',status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, project_pk=None, pk=None, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=pk)
        self.check_object_permissions(self.request, issue)
        serializer = IssueListSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=pk)
        self.check_object_permissions(self.request, issue)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewset(MultipleSerializerMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    detail_serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated & CommentPermission]

    def get_queryset(self):
        """
        Only a contributor of the project can get the list of comments on an issue.
        :return: list of comments for the issue in param
        """
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.check_object_permissions(self.request, project)
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        """
        Add actions to execute during the saving of the instance:
        - save the request.user as the author
        """
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.check_object_permissions(self.request, project)
        comment = serializer.save(author=self.request.user)

    def retrieve(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewset(MultipleSerializerMixin, viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated & ContributorPermission]

    def get_queryset(self):
        project = get_object_or_404(Project,pk=self.kwargs['project_pk'])
        self.check_object_permissions(self.request, project)
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        """
        Add a user to a project as a contributor if :
        - the user exists in the database
        - the user is not already a contributor of this project.
        """
        project = get_object_or_404(Project,pk=self.kwargs['project_pk'])
        self.check_object_permissions(self.request, project)
        contributor = serializer.save()

    def retrieve(self, request, project_pk=None, pk=None, *args, **kwargs):
        contrib = get_object_or_404(Contributor, pk=pk)
        self.check_object_permissions(self.request, contrib)
        serializer = ContributorSerializer(contrib)
        return Response(serializer.data)

    def update(self, request, project_pk=None, pk=None, *args, **kwargs):
        contrib = get_object_or_404(Contributor, pk=pk)
        self.check_object_permissions(self.request, contrib)
        serializer = ContributorSerializer(contrib, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None):
        contrib = get_object_or_404(Contributor, pk=pk)
        self.check_object_permissions(self.request, contrib)
        contrib.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)