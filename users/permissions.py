from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_permission, has_role


class HasCoursePermission(BasePermission):
    """
    Permission class that checks whether a user has a specific role-based permission.

    To use this in a view, set the `required_permission` attribute on the view class,
    for example:

        class SomeCourseView(APIView):
            permission_classes = [HasCoursePermission]
            required_permission = 'edit_course'

    The permission will be checked based on the user's assigned role and its available permissions.
    """

    def has_permission(self, request, view):
        # Retrieve required permission name from the view
        required_permission = getattr(view, 'required_permission', None)

        # Deny access if no required_permission is defined
        if not required_permission:
            return False

        # Check permission using django-role-permissions
        return has_permission(request.user, required_permission)


class IsAdmin(BasePermission):
    """
    Custom permission to check if the user has the 'admin' role.

    Can be used to protect views that should only be accessible to users with
    administrative privileges. This relies on django-role-permissions for role checking.
    """

    def has_permission(self, request, view):
        # Grant access only if the user has the 'admin' role
        return has_role(request.user, 'admin')
