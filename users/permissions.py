from django.contrib.auth import get_user, get_user_model
from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_role

from icecream import ic

User = get_user_model()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == User.Role.ADMIN) and
            has_role(request.user, 'admin')
        )

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == User.Role.STUDENT) and
            has_role(request.user, 'student')
        )

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == User.Role.MODERATOR) and
            has_role(request.user, 'moderator')
        )

