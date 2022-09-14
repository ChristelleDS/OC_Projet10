from rest_framework import permissions
from .models import Contributor, Project


def check_contributor(user, project):
    """
    Check if a user is a contributor of the project
    :param user:
    :param project:
    :return: True if the user is a contributor
    """
    for contributor in Contributor.objects.filter(project_id=project.id):
        if user == contributor.user_id:
            return True
    return False


class ProjectPermission(permissions.BasePermission):
    """
    All users can create a project.
    Authors can also read, update and delete a project.
    Contributors can list theirs projects, read a project
    """
    message = 'Unauthorized action for this user.'

    def has_permission(self, request, view):
        """
        :return: True if user authenticated
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a contributor on the project.
        - can read data
        Check if the user is the author of the object.
        - can update and delete data
        :return: True if authorized user
        """
        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, obj)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id


class IssuePermission(permissions.BasePermission):
    """
    Authors of issues can update and delete it.
    Project contributors can list all project issues, read and create issues.
    """
    message = 'Unauthorized action for this user.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.project_id)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id


class CommentPermission(permissions.BasePermission):
    """
    Comment authors can update or delete their comments.
    Project contributors can read or create comments.
    """

    message = 'Unauthorized action for this user.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.issue_id.project_id)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id


class ContributorPermission(permissions.BasePermission):
    """
    Contributors can list/read other contributors
    Authors of the project can read, add, update or delelete a contributor
    """
    message = 'Unauthorized action for this user.'

    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, Project.objects.filter(id=view.kwargs['projects_pk']).first())

        elif view.action in ['update', 'partial_update', 'create', 'destroy']:
            return request.user == Project.objects.filter(id=view.kwargs['projects_pk']).first().author
