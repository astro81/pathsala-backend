from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rolepermissions.roles import assign_role

from users.permissions import IsAdmin
from users.serializers import UserSerializer
from users.utils import get_user_or_403, is_superuser_blocked

User = get_user_model()


class RegisterUserView(APIView):
    """
    API endpoint for user registration.

    Allows unauthenticated users to register.
    Automatically assigns the "student" role to newly created users.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user.

        Request body:
            - username: str
            - email: str
            - password: str
            - other optional user fields

        Returns:
            - 201: User created successfully.
            - 400: Validation or input error.
            - 500: Internal server error.
        """
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            assign_role(user, 'student')  # Assign default role
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            # DRF handles serializer validation errors here
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as ie:
            return Response(
                {'error': 'Database integrity error. Possibly duplicate or invalid data.', 'details': str(ie)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except DatabaseError as db_err:
            return Response(
                {'error': 'A database error occurred.', 'details': str(db_err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            # Catch-all for any unexpected errors
            return Response(
                {'error': 'An unexpected error occurred.', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginUserView(APIView):
    """
    API endpoint for user login.

    Authenticates user and returns a token for authenticated access to other endpoints.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate user and return a token.

        Request body:
            - username: str
            - password: str

        Returns:
            - 200: Token if credentials are valid.
            - 400: Error if credentials are invalid or missing.
            - 403: Inactive user.
            - 500: Internal server error
        """
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username:
                raise ValidationError({"username": "Username is required."})
            if not password:
                raise ValidationError({"password": "Password is required."})

            user = authenticate(username=username, password=password)

            if not user:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                return Response({'error': 'User account is inactive.'}, status=status.HTTP_403_FORBIDDEN)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)

        except (DatabaseError, IntegrityError) as db_err:
            return Response(
                {'error': 'Database error during login.', 'details': str(db_err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred during login.', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutUserView(APIView):
    """
    API endpoint for logging out.

    Deletes the user's auth token to revoke access.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Invalidate user's token.

        Returns:
            - 200: Success message.
            - 401: If user is not authenticated.
            - 500: If unexpected error occurs.
        """
        try:
            # Attempt to delete the user's token
            request.user.auth_token.delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

        except AttributeError:
            # If user has no token (shouldn't happen with IsAuthenticated but possible)
            raise NotAuthenticated(detail="User token not found.")

        except ObjectDoesNotExist:
            # Token might already be deleted (e.g., logged out from another device)
            return Response({'error': 'Token already deleted or does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred during logout.', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateModeratorView(APIView):
    """
    API endpoint for creating moderator accounts.

    Restricted to users with the 'admin' role.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        """
        Create a new moderator.

        Request body:
            - Same as standard user registration fields.

        Returns:
            - 201: Moderator created.
            - 400: Validation or input error.
            - 500: Unexpected error.
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # DRF-native validation

            user = serializer.save()
            assign_role(user, 'moderator')

            return Response({'message': 'Moderator created successfully'}, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as ie:
            return Response({'error': 'Database integrity error.', 'details': str(ie)}, status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_err:
            return Response({'error': 'Database error occurred.', 'details': str(db_err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': 'Unexpected error occurred.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditUserView(APIView):
    """
    API endpoint to update user profile.

    Users can edit their own profile. Admins can edit any user's profile.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, username=None):
        """
        Fully update a user's profile (all fields required).
        """
        return self._update_user(request, username, full_update=True)

    def patch(self, request, username=None):
        """
        Partially update a user's profile (some fields).
        """
        return self._update_user(request, username, full_update=False)

    def _update_user(self, request, username, full_update):
        """
        Internal handler for both PUT and PATCH operations.
        """
        user = get_user_or_403(request, username)
        if isinstance(user, Response):
            return user  # Already a Response (403/404)

        superuser_block = is_superuser_blocked(user)
        if superuser_block:
            return superuser_block

        try:
            serializer = UserSerializer(user, data=request.data, partial=not full_update)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'User updated successfully.'}, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as ie:
            return Response({'error': 'Database integrity error.', 'details': str(ie)}, status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_err:
            return Response({'error': 'Database error occurred.', 'details': str(db_err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': 'Unexpected error occurred.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUserView(APIView):
    """
    API endpoint to soft delete user accounts.

    Users can deactivate their own account. Admins can deactivate any non-superuser.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, username=None):
        """
        Deactivate a user (soft delete).

        Parameters:
            - username: Optional[str] (default to current user)

        Returns:
            - 200: Deactivated.
            - 403: Not authorized.
            - 404: User not found.
        """
        user = get_user_or_403(request, username)
        if isinstance(user, Response):
            return user

        superuser_block = is_superuser_blocked(user)
        if superuser_block:
            return superuser_block

        try:
            if not user.is_active:
                return Response({'message': 'User is already deactivated.'}, status=status.HTTP_200_OK)

            user.is_active = False
            user.save()

            return Response({'message': 'User deactivated successfully.'}, status=status.HTTP_200_OK)

        except DatabaseError as db_err:
            return Response({'error': 'Database error occurred.', 'details': str(db_err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': 'Unexpected error occurred.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    """
    API endpoint to view user profiles.

    Users can view their own profile. Admins can view any profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        """
        Retrieve user profile.

        Parameters:
            - username: Optional[str] (defaults to current user)

        Returns:
            - 200: User data.
            - 403/404: Not allowed or not found.
            - 500: Internal server error
        """
        try:
            user = get_user_or_403(request, username)
            if isinstance(user, Response):
                return user

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except (DatabaseError, IntegrityError) as db_err:
            return Response(
                {'error': 'Database error while retrieving profile.', 'details': str(db_err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred while retrieving profile.', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

