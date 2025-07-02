"""
User Management API Views

This module implements all user-related API endpoints including:
- Authentication (login/logout)
- Registration (student/moderator)
- Profile management
- User administration
- Filtering and searching

The views follow REST conventions and implement proper:
- Authentication
- Authorization
- Input validation
- Error handling
- Security controls
"""

from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rolepermissions.roles import remove_role, assign_role

from users.models import Student, Moderator
from users.permissions import IsAdmin, IsStudent, IsModerator
from users.serializers import StudentSerializer, UserSerializer, ModeratorSerializer

User = get_user_model()


class LoginView(APIView):
    """Handle user authentication and JWT token generation.

    This view:
    - Validates username/password credentials
    - Authenticates the user
    - Generates JWT tokens upon successful authentication
    - Handles inactive user accounts

    Permissions:
        AllowAny: Accessible to all users

    Methods:
        post: Authenticate user and return tokens
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Authenticate user with username/password and receive JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='User identifier'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password', format='password')
            }
        ),
        responses={
            200: openapi.Response(
                description="Successful authentication",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                        'role': openapi.Schema(type=openapi.TYPE_STRING, description='User role')
                    }
                )
            ),
            400: openapi.Response(
                description="Missing or invalid credentials",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            401: openapi.Response(
                description="Invalid credentials or inactive account",
                examples={
                    "application/json": {
                        "error": "Invalid credentials"
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        """Authenticate the user and return JWT tokens.

        Parameters
        ----------
        request : Request
            Contains:
                username: string (required)
                password: string (required)

        Returns
        -------
        Response
            200: Success with tokens and user's role
            400: Missing credentials
            401: Invalid credentials or inactive account
            500: Server error
        """
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username:
                raise ValidationError({"error": "Username is required"})
            if not password:
                raise ValidationError({"error": "Password is required"})

            user = authenticate(username=username, password=password)

            if not user:
                raise ValidationError({"error": "Invalid credentials"})

            if not user.is_active:
                return Response(
                    {"error": "User is inactive"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    """Handle user logout by blacklisting refresh token.

    This view:
    - Invalidates the provided refresh token
    - Effectively logs the user out of the current session

    Permissions:
        IsAuthenticated: Only logged-in users can logout

    Methods:
        post: Blacklist the provided refresh token
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Logout by invalidating the refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Refresh token to invalidate'
                )
            }
        ),
        responses={
            205: openapi.Response(
                description="Successfully logged out",
                examples={
                    "application/json": {
                        "message": "Successfully logged out"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid or missing token",
                examples={
                    "application/json": {
                        "error": "Refresh token is required"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Authentication']
    )
    def post(self, request):
        """Invalidate the provided refresh token.

        Parameters
        ----------
        request : Request
            Contains:
                refresh_token: string (required)

        Returns
        -------
        Response
            205: Successful logout
            400: Missing or invalid token
            500: Server error
        """
        try:
            refresh_token = request.data["refresh_token"]
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutAllView(APIView):
    """Handle user logout from all devices.

    This view:
    - Blacklists all outstanding tokens for the user
    - Effectively logs the user out from all sessions

    Permissions:
        IsAuthenticated: Only logged-in users can logout

    Methods:
        post: Blacklist all tokens for the current user
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Logout from all devices by invalidating all refresh tokens",
        responses={
            205: openapi.Response(
                description="Successfully logged out from all devices",
                examples={
                    "application/json": {
                        "message": "Successfully logged out from all devices"
                    }
                }
            ),
            200: openapi.Response(
                description="No active tokens found",
                examples={
                    "application/json": {
                        "message": "No active tokens found"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Authentication']
    )
    def post(self, request):
        """Invalidate all tokens for the current user.

        Parameters
        ----------
        request : Request
            None required in body

        Returns
        -------
        Response
            205: Successful logout from all devices
            200: No active tokens found
            500: Server error
        """
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            if not tokens.exists():
                return Response(
                    {"message": "No active tokens found"},
                    status=status.HTTP_200_OK,
                )

            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response(
                {"message": "Successfully logged out from all devices"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StudentRegisterView(APIView):
    """Handle student registration.

    This view:
    - Creates new student accounts
    - Validates input data
    - Assigns student role
    - Handles errors appropriately

    Permissions:
        AllowAny: Accessible to all users

    Methods:
        post: Create a new student account
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Register a new student account",
        request_body=StudentSerializer,
        responses={
            201: openapi.Response(
                description="Student created successfully",
                examples={
                    "application/json": {
                        "message": "Student created successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                schema=StudentSerializer,
                examples={
                    "application/json": {
                        "username": ["This field is required."],
                        "email": ["Enter a valid email address."]
                    }
                }
            )
        },
        tags=['Registration']
    )
    def post(self, request):
        """Register a new student account.

        Parameters
        ----------
        request : Request
            Contains student registration data

        Returns
        -------
        Response
            201: Student created successfully
            400: Validation error
            500: Server error
        """
        try:
            serializer = StudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Student created successfully"},
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"error": "Database integrity error occurred"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DatabaseError:
            return Response(
                {"error": "Database operation failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModeratorRegisterView(APIView):
    """Handle moderator registration.

    This view:
    - Creates new moderator accounts (admin only)
    - Validates input data
    - Assigns moderator role
    - Handles errors appropriately

    Permissions:
        IsAdmin: Only administrators can create moderators

    Methods:
        post: Create a new moderator account
    """

    permission_classes = (IsAdmin,)

    @swagger_auto_schema(
        operation_description="Register a new moderator account (admin only)",
        request_body=ModeratorSerializer,
        responses={
            201: openapi.Response(
                description="Moderator created successfully",
                examples={
                    "application/json": {
                        "message": "Moderator created successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                schema=ModeratorSerializer
            ),
            403: openapi.Response(
                description="Permission denied",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Registration']
    )
    def post(self, request):
        """Register a new moderator account.

        Parameters
        ----------
        request : Request
            Contains moderator registration data

        Returns
        -------
        Response
            201: Moderator created successfully
            400: Validation error
            403: Permission denied
            500: Server error
        """
        try:
            serializer = ModeratorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"message": "Moderator created successfully"},
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"error": "Database integrity error occurred"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DatabaseError:
            return Response(
                {"error": "Database operation failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserOwnProfileView(APIView):
    """Handle retrieval of the current user's profile.

    This view:
    - Returns profile data for the authenticated user
    - Includes student-specific fields if applicable
    - Handles profile picture URL generation

    Permissions:
        IsAuthenticated: Only logged-in users can view their profile

    Methods:
        get: Retrieve current user's profile
    """

    permission_classes = (IsAuthenticated,)


    @swagger_auto_schema(
        operation_description="Get the authenticated user's profile information",
        responses={
            200: openapi.Response(
                description="User profile data",
                schema=UserSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "student1",
                        "email": "student@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "role": "student",
                        "is_active": True,
                        "address": "123 Main St",
                        "phone_no": "+1234567890",
                        "is_approved": True,
                        "profile_picture": "http://example.com/media/profile_pics/student1.jpg"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Profile']
    )
    def get(self, request):
        """Get the authenticated user's profile.

        Parameters
        ----------
        request : Request
            None required in body

        Returns
        -------
        Response
            200: User profile data
            500: Server error
        """
        try:
            user = request.user
            serialized_user = UserSerializer(user).data

            # Add student-specific data if applicable
            if user.role == user.Role.STUDENT:
                try:
                    student = Student.objects.get(user=user)
                    profile_data = {
                        "address": student.address,
                        "phone_no": student.phone_no,
                        "is_approved": student.is_approved,
                    }

                    if student.profile_picture:
                        try:
                            profile_data["profile_picture"] = request.build_absolute_uri(
                                student.profile_picture.url
                            )
                        except Exception:
                            profile_data["profile_picture"] = None

                    serialized_user.update(profile_data)

                except ObjectDoesNotExist:
                    pass

            return Response(serialized_user, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminUserDetailView(APIView):
    """Handle user profile retrieval by administrators.

    This view:
    - Returns profile data for any user (admin only)
    - Includes role-specific fields
    - Handles profile picture URL generation

    Permissions:
        IsAdmin: Only administrators can view other users' profiles

    Methods:
        get: Retrieve user profile by username
    """

    permission_classes = (IsAdmin,)

    @swagger_auto_schema(
        operation_description="Get user profile by username (admin only)",
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_PATH,
                description="Username of the user to retrieve",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="User profile data",
                schema=UserSerializer
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Administration']
    )
    def get(self, request, username):
        """Get a user's profile by username.

        Parameters
        ----------
        request : Request
            None required in body
        username : str
            Username of the user to retrieve

        Returns
        -------
        Response
            200: User profile data
            404: User not found
            500: Server error
        """
        try:
            user = get_object_or_404(User, username=username)
            data = UserSerializer(user).data

            if user.role == user.Role.STUDENT:
                try:
                    student = Student.objects.get(user=user)
                    profile_data = {
                        "address": student.address,
                        "phone_no": student.phone_no,
                        "is_approved": student.is_approved,
                    }

                    if student.profile_picture:
                        try:
                            profile_data["profile_picture"] = request.build_absolute_uri(
                                student.profile_picture.url
                            )
                        except Exception:
                            profile_data["profile_picture"] = None

                    data.update(profile_data)

                except ObjectDoesNotExist:
                    pass
            else:
                data.update(
                    {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role,
                    }
                )

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StudentProfileUpdateView(APIView):
    """Handle student profile updates.

    This view:
    - Allows students to update their profiles
    - Validates input data
    - Handles partial updates

    Permissions:
        IsStudent: Only students can update their profiles

    Methods:
        patch: Partially update student profile
    """

    permission_classes = (IsStudent,)
    parser_classes = [MultiPartParser, FormParser]  # Enables file upload

    @swagger_auto_schema(
        operation_description="Update student profile information",
        request_body=StudentSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                examples={
                    "application/json": {
                        "message": "Profile successfully updated!"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                schema=StudentSerializer
            ),
            404: openapi.Response(
                description="Profile not found",
                examples={
                    "application/json": {
                        "message": "Student profile not found"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Profile']
    )
    def patch(self, request):
        """Update the student's profile.

        Parameters
        ----------
        request : Request
            Contains profile fields to update

        Returns
        -------
        Response
            200: Profile updated successfully
            400: Validation error
            404: Profile not found
            500: Server error
        """
        try:
            user = request.user
            student = Student.objects.get(user=user)

            serializer = StudentSerializer(
                student, data=request.data, partial=True, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"message": "Profile successfully updated!"}, status=status.HTTP_200_OK
            )

        except ObjectDoesNotExist:
            return Response(
                {"message": "Student profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModeratorProfileUpdateView(APIView):
    """Handle moderator profile updates.

    This view:
    - Allows moderators to update their profiles
    - Validates input data
    - Handles partial updates

    Permissions:
        IsModerator: Only moderators can update their profiles

    Methods:
        patch: Partially update moderator profile
    """

    permission_classes = (IsModerator,)
    parser_classes = [MultiPartParser, FormParser]  # Enables file upload

    @swagger_auto_schema(
        operation_description="Update moderator profile information",
        request_body=ModeratorSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                examples={
                    "application/json": {
                        "message": "Profile successfully updated!"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                schema=ModeratorSerializer
            ),
            404: openapi.Response(
                description="Profile not found",
                examples={
                    "application/json": {
                        "message": "Moderator profile not found"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Profile']
    )
    def patch(self, request):
        """Update the moderator's profile.

        Parameters
        ----------
        request : Request
            Contains profile fields to update

        Returns
        -------
        Response
            200: Profile updated successfully
            400: Validation error
            404: Profile not found
            500: Server error
        """
        try:
            user = request.user
            moderator = Moderator.objects.get(user=user)

            serializer = ModeratorSerializer(
                moderator, data=request.data, partial=True, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"message": "Profile successfully updated!"}, status=status.HTTP_200_OK
            )

        except ObjectDoesNotExist:
            return Response(
                {"message": "Moderator profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def delete_token_helper(user):
    """Helper function to invalidate all tokens for a user.

    Parameters
    ----------
    user : User
        User whose tokens should be invalidated
    """
    for token in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=token)


def delete_user_role_helper(user):
    """Helper function to remove role assignments from a user.

    Parameters
    ----------
    user : User
        User whose roles should be removed
    """
    if user.role == User.Role.STUDENT:
        remove_role(user, "student")
    if user.role == User.Role.MODERATOR:
        remove_role(user, "moderator")


class UserDeleteView(APIView):
    """Handle user account deletion (self-service).

    This view:
    - Allows users to delete their own accounts
    - Requires password confirmation
    - Performs soft deletion (sets is_active=False)
    - Invalidates all tokens
    - Removes role assignments

    Permissions:
        IsAuthenticated: Only logged-in users can delete their accounts

    Methods:
        delete: Delete the user's account
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Delete the authenticated user's account (requires password confirmation)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username for confirmation'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Password for confirmation',
                    format='password'
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Account deleted successfully",
                examples={
                    "application/json": {
                        "message": "Account deleted successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Missing or invalid credentials",
                examples={
                    "application/json": {
                        "error": "Username is required"
                    }
                }
            ),
            401: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "error": "Invalid credentials"
                    }
                }
            ),
            403: openapi.Response(
                description="Role not allowed to self-delete",
                examples={
                    "application/json": {
                        "message": "Only moderators and students can delete their account"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Profile']
    )
    def delete(self, request):
        """Delete the authenticated user's account.

        Parameters
        ----------
        request : Request
            Contains:
                username: string (required for confirmation)
                password: string (required for confirmation)

        Returns
        -------
        Response
            200: Account deleted successfully
            400: Missing/invalid credentials
            401: Invalid credentials
            403: Role not allowed to self-delete
            500: Server error
        """
        try:
            user = request.user
            username = request.data.get("username")
            password = request.data.get("password")

            if not username:
                return Response(
                    {"error": "Username is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not password:
                return Response(
                    {"error": "Password is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if user.username != username:
                return Response(
                    {"error": "Username does not match the logged in user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            authenticated_user = authenticate(username=username, password=password)
            if (not authenticated_user) or (authenticated_user != user):
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if user.role not in [User.Role.MODERATOR, User.Role.STUDENT]:
                return Response(
                    {"message": "Only moderators and students can delete their account"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            delete_token_helper(user)
            delete_user_role_helper(user)

            user.is_active = False
            user.save()

            return Response(
                {"message": "Account deleted successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminDeleteUserView(APIView):
    """Handle user deletion by administrators.

    This view:
    - Allows admins to delete other user accounts
    - Requires username confirmation
    - Prevents admin self-deletion
    - Can perform soft or hard deletion based on flag
    - Invalidates all tokens
    - Removes role assignments

    Permissions:
        IsAdmin: Only administrators can delete users

    Methods:
        delete: Delete a user account
    """

    permission_classes = (IsAdmin,)
    permanently_delete = False  # Flag for hard vs soft deletion

    @swagger_auto_schema(
        operation_description="Deactivate a user account (admin only)",
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="ID of the user to deactivate",
                type=openapi.TYPE_INTEGER
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username for confirmation'
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="User deactivated successfully",
                examples={
                    "application/json": {
                        "message": "User deactivated successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Missing/invalid confirmation",
                examples={
                    "application/json": {
                        "error": "Confirmation username does not match"
                    }
                }
            ),
            403: openapi.Response(
                description="Attempted self-deletion",
                examples={
                    "application/json": {
                        "message": "You cannot delete the admin account"
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "message": "User not found"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Administration']
    )
    def delete(self, request, user_id):
        """Delete a user account by ID.

        Parameters
        ----------
        request : Request
            Contains:
                username: string (required for confirmation)
        user_id : int
            ID of the user to delete

        Returns
        -------
        Response
            200: User deleted/deactivated successfully
            400: Missing/invalid confirmation
            403: Attempted self-deletion
            404: User not found
            500: Server error
        """
        try:
            admin = request.user
            user = get_object_or_404(User, pk=user_id)

            # Get confirmation username from request data
            confirm_username = request.data.get("username")

            # Validate confirmation username
            if not confirm_username:
                return Response(
                    {
                        "error": "Please provide the username of the user you want to delete as confirmation"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Verify username matches the user being deleted
            if confirm_username != user.username:
                return Response(
                    {
                        "error": "Confirmation username does not match the user you're trying to delete"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Prevent deletion of the admin account
            if user.id == admin.id:
                return Response(
                    {"message": "You cannot delete the admin account"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            delete_token_helper(user)
            delete_user_role_helper(user)

            if self.permanently_delete:  # Hard delete
                user.delete()
                message = "User permanently deleted!"
            else:  # Softly delete
                user.is_active = False
                user.save()
                message = "User deactivated successfully!"

            return Response({"message": message}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReactivateUserView(APIView):
    """Handle user account reactivation by administrators.

    This view:
    - Reactivates deactivated accounts
    - Restores original role assignments
    - Handles errors appropriately

    Permissions:
        IsAdmin: Only administrators can reactivate accounts

    Methods:
        post: Reactivate a user account
    """

    permission_classes = (IsAdmin,)

    @swagger_auto_schema(
        operation_description="Reactivate a deactivated user account (admin only)",
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="ID of the user to reactivate",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Account reactivated successfully",
                examples={
                    "application/json": {
                        "message": "Account reactivated successfully with original role"
                    }
                }
            ),
            404: openapi.Response(
                description="Inactive user not found",
                examples={
                    "application/json": {
                        "message": "Inactive user not found"
                    }
                }
            )
        },
        security=[{'Bearer': []}],
        tags=['Administration']
    )
    def post(self, request, user_id):
        """Reactivate a deactivated user account.

        Parameters
        ----------
        request : Request
            None required in body
        user_id : int
            ID of the user to reactivate

        Returns
        -------
        Response
            200: Account reactivated successfully
            404: User not found
            500: Server error
        """
        try:
            # Get the inactive user
            user = get_object_or_404(User, pk=user_id, is_active=False)

            # Reactivate the account
            user.is_active = True
            user.save()

            # Restore the appropriate role based on the user's role field
            if user.role == User.Role.MODERATOR:
                assign_role(user, "moderator")
            if user.role == User.Role.STUDENT:
                assign_role(user, "student")

            return Response(
                {"message": "Account reactivated successfully with original role"},
                status=status.HTTP_200_OK,
            )

        except ObjectDoesNotExist:
            return Response(
                {"message": "Inactive user not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserFilter(filters.FilterSet):
    """FilterSet for advanced user filtering.

    Provides filtering capabilities for the User model including:
    - Role-based filtering
    - Status flags (active, staff, superuser)
    - Date ranges (joined, last login)
    - Text search (username, email, names)
    - Multiple choice filters

    Example usage:
    /api/users/?role=student
    /api/users/?roles=student,moderator
    /api/users/?date_joined__gte=2023-01-01
    /api/users/?username__icontains=admin
    """

    role = filters.ChoiceFilter(choices=User.Role.choices)
    is_active = filters.BooleanFilter()
    is_staff = filters.BooleanFilter()
    is_superuser = filters.BooleanFilter()

    # Date filters
    date_joined = filters.DateFromToRangeFilter()
    last_login = filters.DateFromToRangeFilter()

    # Text-based filters
    username = filters.CharFilter(lookup_expr="icontains")
    email = filters.CharFilter(lookup_expr="icontains")
    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")

    # Multiple choice filters
    roles = filters.MultipleChoiceFilter(
        field_name="role", choices=User.Role.choices
    )

    class Meta:
        model = User
        fields = [
            "role",
            "roles",
            "is_active",
            "is_staff",
            "is_superuser",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
        ]


class UserListAPIView(ListAPIView):
    """API endpoint for listing and filtering users.

    Provides comprehensive user listing with:
    - Advanced filtering (UserFilter)
    - Search capabilities
    - Ordering options
    - Pagination

    Permissions:
        IsAdmin: Only administrators can list users

    Methods:
        get: List users with optional filtering
    """

    queryset = User.objects.all().select_related().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    # Filter backends
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Filter configuration
    filterset_class = UserFilter

    # Search configuration
    search_fields = ["username", "email", "first_name", "last_name"]

    # Ordering configuration
    ordering_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "date_joined",
        "last_login",
    ]
    ordering = ["-date_joined"]  # Default ordering

    @swagger_auto_schema(
        operation_description="List and filter users (admin only)",
        manual_parameters=[
            openapi.Parameter(
                'role',
                openapi.IN_QUERY,
                description="Filter by user role",
                type=openapi.TYPE_STRING,
                enum=['student', 'moderator', 'admin']
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filter by active status",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                description="Filter by username (contains)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'date_joined__gte',
                openapi.IN_QUERY,
                description="Filter users joined after this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Ordering field (prefix with - for descending)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="List of users",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=UserSerializer
                        )
                    }
                )
            )
        },
        security=[{'Bearer': []}],
        tags=['User Listing']
    )
    def list(self, request, *args, **kwargs):
        """Override list method for a custom response format.

        Parameters
        ----------
        request : Request
            May contain filtering/ordering parameters

        Returns
        -------
        Response
            200: Success with user data
            500: Server error
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return Response(
                {
                    "success": True,
                    "count": queryset.count(),
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": "Failed to retrieve users",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

