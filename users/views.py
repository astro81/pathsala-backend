from datetime import timezone
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError, DatabaseError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role

from users.permissions import IsAdmin
from users.serializers import UserSerializer
from users.utils import get_user_or_403, is_superuser_blocked, invalidate_user_tokens

User = get_user_model()


class RegisterUserView(APIView):
    """
    API endpoint for user registration.

    Allows unauthenticated users to register.
    Automatically assigns the "student" role to newly created users.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: openapi.Response("User registered successfully"),
            400: "Validation or input error",
            500: "Internal server error"
        }
    )
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

    Authenticates a user and returns a token for authenticated access to other endpoints.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="User login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: openapi.Response("Token returned"),
            400: "Invalid credentials",
            403: "Inactive user",
            500: "Internal error"
        }
    )
    def post(self, request):
        """
        Authenticate a user and return a token.

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

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

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

    @swagger_auto_schema(
        operation_summary="Logout user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Logout successful",
            400: "Missing or invalid token",
            500: "Unexpected error"
        }
    )



    def post(self, request):
        """
        Invalidate user's token.

        Returns:
            - 200: Success message.
            - 401: If the user is not authenticated.
            - 500: If an unexpected error occurs.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Logout Successfully."},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"Error":"Already Logout."},status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    """
    API endpoint to refresh access token using refresh token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Refresh access token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: openapi.Response("New access token"),
            401: "Invalid refresh token",
            500: "Error"
        }
    )
    def post(self, request):
        """
        Generate a new access token from refresh token.
        """
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except TokenError as te:
            return Response(
                {'error': 'Invalid or expired refresh token.', 'details': str(te)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {'error': 'Token refresh failed.', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateModeratorView(APIView):
    """
    API endpoint for creating moderator accounts.

    Restricted to users with the 'admin' role.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: "Moderator created",
            400: "Validation error",
            500: "Unexpected error"
        }
    )
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

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: "User updated", 400: "Validation error", 500: "Error"}
    )
    def put(self, request, username=None):
        """
        Fully update a user's profile (all fields required).
        """
        return self._update_user(request, username, full_update=True)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: "User updated", 400: "Validation error", 500: "Error"}
    )
    def patch(self, request, username=None):
        """
        Partially update a user's profile (some fields).
        """
        return self._update_user(request, username, full_update=False)

    def _update_user(self, request, username, full_update):
        """
        Internal handler for both PUT and PATCH operations.
        """
        # Resolve user object or return appropriate error (403 or 404)
        user = get_user_or_403(request, username)
        if isinstance(user, Response):
            return user

        # Prevent superuser updates in restricted contexts
        superuser_block = is_superuser_blocked(user)
        if superuser_block:
            return superuser_block

        try:
            # Check if the password is being changed
            is_password_changed = False
            if 'password' in request.data:
                if not user.check_password(request.data.get('password')):
                    is_password_changed = True

            # Validate and save user data
            serializer = UserSerializer(user, data=request.data, partial=not full_update)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Invalidate tokens if the password has changed
            if is_password_changed:
                invalidate_user_tokens(user)
                return Response({
                    'message': 'User updated successfully. Please login again with your new password.',
                    'logout_required': True
                }, status=status.HTTP_200_OK)

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
    API endpoint to softly delete user accounts.

    Users can deactivate their own account. Admins can deactivate any non-superuser.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "User deactivated",
            403: "Not allowed",
            404: "User not found",
            500: "Error"
        }
    )
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


class ReactivateUserView(APIView):
    """
    API endpoint to reactivate (enable) a previously deactivated user account.

    Permissions:
        - Only authenticated users with admin privileges can reactivate accounts.

    HTTP Methods:
        - POST: Reactivate the user specified by username.

    Parameters:
        - username (str, optional): The username of the user to reactivate.
          If not provided, defaults to the current user (can be adjusted as needed).

    Responses:
        - 200 OK: If the user is successfully reactivated or already active.
        - 404 Not Found or 403 Forbidden: If the user does not exist or is inaccessible.
        - 500 Internal Server Error: For unexpected errors during reactivation.
    """
    permission_classes = [IsAuthenticated, IsAdmin]  # Restrict access to authenticated admins

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: "User reactivated",
            403: "Permission denied",
            404: "User not found",
            500: "Error"
        }
    )
    def post(self, request, username=None):
        """
        Handle POST request to reactivate a user account.

        Args:
            request (Request): DRF request object.
            username (str, optional): Target user's username.

        Returns:
            Response: DRF response with a success or error message.
        """
        # Retrieve the target user or return the appropriate 403/404 response
        user = get_user_or_403(request, username)
        if isinstance(user, Response):
            return user  # Early return if user retrieval failed

        # Check if the user is already active to avoid unnecessary updates
        if user.is_active:
            return Response(
                {'message': 'User is already active.'},
                status=status.HTTP_200_OK
            )

        try:
            # Reactivate the user by setting is_active to True
            user.is_active = True
            user.save()

            return Response(
                {'message': 'User reactivated successfully.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # Catch all unexpected exceptions and respond with error details
            return Response(
                {'error': 'Unexpected error.', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileView(APIView):
    """
    API endpoint to view user profiles.

    Users can view their own profile. Admins can view any profile.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response("User data", UserSerializer),
            403: "Forbidden",
            404: "Not found",
            500: "Error"
        }
    )
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

class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        operation_summary="List users",
        manual_parameters=[
            openapi.Parameter(
                'role',
                openapi.IN_QUERY,
                description="Optional user role to filter by (e.g. 'student')",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: UserSerializer(many=True)}
    )
    def get_queryset(self):
        role = self.request.query_params.get('role')
        users = User.objects.all().order_by('username')

        if role:
            # Filter users in Python to those with the requested role
            # But first limit queryset to a manageable size for performance
            # Here we do full queryset and filter below in a pagination step
            self.role = role
            return users

        self.role = None
        return users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if self.role:
            # Filter users who have the specified role
            filtered_users = [user for user in queryset if has_role(user, self.role)]
        else:
            filtered_users = list(queryset)

        page = self.paginate_queryset(filtered_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_users, many=True)
        return Response(serializer.data)

