from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
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
            - 400: Validation error.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            assign_role(user, 'student')  # Default role assignment
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


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
        """
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


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
            - 400: Validation error.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            assign_role(user, 'moderator')
            return Response({'message': 'Moderator created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserView(APIView):
    """
    API endpoint to update user profile.

    Users can edit their own profile. Admins can edit any user's profile.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, username=None):
        """
        Fully update a user's profile (all fields required).

        Parameters:
            - username: Optional[str] (default to current user if not provided)

        Returns:
            - 200: Updated successfully.
            - 400/403/404: Error.
        """
        return self._update_user(request, username, full_update=True)

    def patch(self, request, username=None):
        """
        Partially update a user's profile (some fields).

        Parameters:
            - username: Optional[str] (default to current user if not provided)

        Returns:
            - 200: Updated successfully.
            - 400/403/404: Error.
        """
        return self._update_user(request, username, full_update=False)

    def _update_user(self, request, username, full_update):
        """
        Internal handler for both PUT and PATCH operations.

        Ensures permission checks and superuser safety.
        """
        user = get_user_or_403(request, username)
        if isinstance(user, Response):
            return user

        superuser_block = is_superuser_blocked(user)
        if superuser_block:
            return superuser_block

        serializer = UserSerializer(user, data=request.data, partial=not full_update)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    """
    API endpoint to delete user accounts.

    Users can delete their own account. Admins can delete any non-superuser.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, username=None):
        """
        Delete a user.

        Parameters:
            - username: Optional[str] (default to current user)

        Returns:
            - 200: Deleted.
            - 403: Not authorized.
            - 404: User not found.
        """
        user = get_user_or_403(request, username)
        if isinstance(user, Response):
            return user

        superuser_block = is_superuser_blocked(user)
        if superuser_block:
            return superuser_block

        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)


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
        """
        user = get_user_or_403(request, username)
        if isinstance(user, Response):
            return user

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
