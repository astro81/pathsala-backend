"""
Authentication and Authorization Utilities

This module provides helper functions for user management and token handling in Django REST Framework.
It includes security-focused utilities for user retrieval, permission checks, and token invalidation.

Functions:
    get_user_or_403: Secure user retrieval with permission checks
    is_superuser_blocked: Protection against superuser modifications
    invalidate_user_tokens: Comprehensive token invalidation
"""

from datetime import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rolepermissions.checkers import has_role

User = get_user_model()


def get_user_or_403(request, username):
    """Retrieve user with proper authorization checks.

    Implements secure user profile access with the following rules:
    1. Users can always access their own profile
    2. Only admin users can access other users' profiles
    3. Returns appropriate HTTP error responses for unauthorized access

    Parameters
    ----------
    request : rest_framework.request.Request
        The incoming request containing the authenticated user
    username : str or None
        Target username to retrieve. If None/empty, returns the requesting user.

    Returns
    -------
    Union[User, Response]
        - User object if access is granted
        - 403 Response if admin privileges are required but missing
        - 404 Response if the target user is not found

    Examples
    --------
    >>> user = get_user_or_403(request, "some_username")
    >>> if isinstance(user, Response):
    ...     return user  # Handle error case
    """
    # Current user access shortcut
    if not username or username == request.user.username:
        return request.user

    # Admin privilege check
    if not has_role(request.user, "admin"):
        return Response(
            {"error": "Admin permissions required."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Target user lookup
    user = User.objects.filter(username=username).first()
    if not user:
        return Response(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

    return user


def is_superuser_blocked(user):
    """Prevent API modifications to superuser accounts.

    Security measure to protect superusers from being modified or deleted
    through regular API endpoints. Should be used as a pre-condition check
    in sensitive operations.

    Parameters
    ----------
    user : User
        User instance to validate

    Returns
    -------
    Union[None, Response]
        - None if the user is not a superuser
        - 403 Response if the user is superuser

    Notes
    -----
    This should be used before update/delete operations:
    >>> if block_response := is_superuser_blocked(target_user):
    ...     return block_response
    """
    if user.is_superuser:
        return Response(
            {"error": "Superuser accounts cannot be modified via API."},
            status=status.HTTP_403_FORBIDDEN,
        )
    return None


def invalidate_user_tokens(user):
    """Completely invalidate all JWT tokens for a user.

    Performs thorough token invalidation by:
    1. Blacklisting all outstanding tokens
    2. Handling both access and refresh tokens
    3. Gracefully handling token expiration

    Parameters
    ----------
    user : User
        User whose tokens should be invalidated

    Returns
    -------
    Union[bool, Response]
        - True if successful
        - 500 Response with error details if failure occurs

    Warnings
    --------
    This action is irreversible and will immediately log out the user
    from all devices. Use with caution.
    """
    try:
        # Method 1: Direct blacklisting via OutstandingToken
        for token in OutstandingToken.objects.filter(user=user):
            if not token.expires_at or token.expires_at > timezone.now():
                BlacklistedToken.objects.get_or_create(token=token)

        # # Method 2: Using SimpleJWT's built-in blacklist
        # for token in OutstandingToken.objects.filter(user=user):
        #     RefreshToken(token.token).blacklist()

        return True
    except Exception as e:
        return Response(
            f"Token invalidation failed for {user.username}: {str(e)}",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

