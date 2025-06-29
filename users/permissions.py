"""
Custom Permission Classes for Django REST Framework

This module implements role-based permission classes that verify both:
1. The user's role is stored in User model
2. The user's permissions in the django-role-permissions system

Classes:
    IsAdmin: Checks for administrator privileges
    IsStudent: Checks for student privileges
    IsModerator: Checks for moderator privileges

The permission system implements defense-in-depth by requiring:
- Authentication
- Correct User.role value
- Corresponding role in django-role-permissions
"""

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_role

# Get the active user model configured in Django
User = get_user_model()


class IsAdmin(BasePermission):
    """Permission class to verify administrator access rights.

    This permission checks that the requesting user:
    1. Is authenticated
    2. Has User.role set to ADMIN
    3. Has the 'admin' role in django-role-permissions

    Example:
        @permission_classes([IsAdmin])
        class AdminViewSet(viewsets.ModelViewSet):
            ...
    """

    def has_permission(self, request, view):
        """Determine if the request has admin-level access.

        Parameters
        ----------
        request : rest_framework.request.Request
            The incoming HTTP request
        view : rest_framework.views.APIView
            The target view being accessed

        Returns
        -------
        bool
            True if the user meets all admin requirements, False otherwise

        Notes
        -----
        All three conditions must be True for access to be granted:
        1. User must be authenticated
        2. User.role must equal User.Role.ADMIN
        3. User must have an 'admin' role in role-permissions
        """
        return (
            request.user.is_authenticated
            and (request.user.role == User.Role.ADMIN)
            and has_role(request.user, 'admin')
        )


class IsStudent(BasePermission):
    """Permission class to verify student access rights.

    This permission checks that the requesting user:
    1. Is authenticated
    2. Has User.role set to STUDENT
    3. Has the 'student' role in django-role-permissions

    Example:
        @permission_classes([IsStudent])
        class StudentDashboard(APIView):
            ...
    """

    def has_permission(self, request, view):
        """Determine if the request has student-level access.

        Parameters
        ----------
        request : rest_framework.request.Request
            The incoming HTTP request
        view : rest_framework.views.APIView
            The target view being accessed

        Returns
        -------
        bool
            True if the user meets all student requirements, False otherwise
        """
        return (
            request.user.is_authenticated
            and (request.user.role == User.Role.STUDENT)
            and has_role(request.user, 'student')
        )


class IsModerator(BasePermission):
    """Permission class to verify moderator access rights.

    This permission checks that the requesting user:
    1. Is authenticated
    2. Has User.role set to MODERATOR
    3. Has the 'moderator' role in django-role-permissions

    Example:
        @permission_classes([IsModerator])
        class ContentModerationView(APIView):
            ...
    """

    def has_permission(self, request, view):
        """Determine if the request has moderator-level access.

        Parameters
        ----------
        request : rest_framework.request.Request
            The incoming HTTP request
        view : rest_framework.views.APIView
            The target view being accessed

        Returns
        -------
        bool
            True if the user meets all moderator requirements, False otherwise
        """
        return (
            request.user.is_authenticated
            and (request.user.role == User.Role.MODERATOR)
            and has_role(request.user, 'moderator')
        )

