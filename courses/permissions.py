from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_permission, has_role

User = get_user_model()


class HasCoursePermission(BasePermission):
    """Custom permission class for role-based course access control.

    This permission class integrates with django-role-permissions to check if a user
    has the required permission based on their assigned role.

    Notes
    -----
    To implement this permission:
    1. Add `permission_classes = [HasCoursePermission]` to your view
    2. Define the ` required_permission ` attribute on the view class
       Example: `required_permission = 'edit_course'`

    The permission system works in conjunction with django-role-permissions roles
    and permissions configuration.

    Methods
    -------
    has_permission(request, view)
        Determines if the requesting user has the required permission.
    """

    def has_permission(self, request, view):
        """Check if the user has the required permission for the requested view.

        Parameters
        ----------
        request : Request
            The incoming request object
        view : APIView
            The view being accessed

        Returns
        -------
        bool
            True if the user has permission, False otherwise

        Notes
        -----
        The method performs these checks in order:
        1. Verifies the view has defined `required_permission` attribute
        2. Checks if the current user has that permission via rolepermissions
        """
        required_permission = getattr(view, 'required_permission', None)

        # Explicitly deny access if no permission is specified
        if not required_permission:
            return False

        return has_permission(request.user, required_permission)

