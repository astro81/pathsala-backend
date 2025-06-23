from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rolepermissions.checkers import has_role

User = get_user_model()


def get_user_or_403(request, username):
    """
    Retrieve a user object based on the provided username with permission checks.

    This utility ensures:
    - A user can access their own account.
    - Only users with the 'admin' role can access other users' data.

    Parameters:
        request (HttpRequest): The incoming request with authenticated user.
        username (str): The username of the user to retrieve. If None, defaults to current user.

    Returns:
        User | Response:
            - User instance if access is allowed.
            - 403 Response if the requester lacks admin privileges.
            - 404 Response if the user does not exist.
    """
    # If no username is provided or requesting own profile, return current user
    if not username or username == request.user.username:
        return request.user

    # Only admins are allowed to access other users' data
    if not has_role(request.user, 'admin'):
        return Response({'error': 'Admin permissions required.'}, status=status.HTTP_403_FORBIDDEN)

    # Attempt to retrieve the target user
    user = User.objects.filter(username=username).first()
    if not user:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    return user


def is_superuser_blocked(user):
    """
    Block access to operations on superuser accounts via API.

    This function can be used to prevent modification or deletion
    of superusers through exposed API endpoints.

    Parameters:
        user (User): The user instance to check.

    Returns:
        None | Response:
            - None if user is not a superuser.
            - 403 Response if the user is a superuser.
    """
    if user.is_superuser:
        return Response(
            {'error': 'Superuser accounts cannot be modified via API.'},
            status=status.HTTP_403_FORBIDDEN
        )
    return None
