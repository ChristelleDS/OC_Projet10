from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Issue, Comment
from .serializers import ProjectListSerializer, ProjectDetailSerializer, \
    IssueListSerializer, IssueDetailSerializer, CommentSerializer


# Create your views here.
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


class ProjectViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.filter()


class AdminProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()


class IssueViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = IssueListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter()


class AdminIssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    queryset = Issue.objects.all()


class CommentViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = IssueListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter()
