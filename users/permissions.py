from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_permission, has_role


class HasCoursePermission(BasePermission):
    """
    Base permission checker using django-role-permissions.
    You must pass the required role permission name to the view via `required_permission` attribute.
    """

    def has_permission(self, request, view):
        required_permission = getattr(view, 'required_permission', None)

        if not required_permission:
            return False

        return has_permission(request.user, required_permission)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, 'admin')