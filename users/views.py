from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role

from users.permissions import IsAdmin
from users.serializers import UserSerializer

User = get_user_model()


# Create your views here.
class RegisterUserView(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            assign_role(user, 'student')    #! force student role

            return Response(
                {'message': 'User registered successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = AllowAny,
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Login Failed!\nInvalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    permission_classes = IsAuthenticated,

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class CreateModeratorView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            assign_role(user, 'moderator')

            return Response(
                {'message': 'Moderator created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, username=None):
        return self.update_user(request, username, full_update=True)

    def patch(self, request, username=None):
        return self.update_user(request, username, full_update=False)

    def update_user(self, request, username, full_update):
        # Handle self-edit
        if not username:
            user = request.user
        else:
            # Reject if not admin and trying to edit others
            if username != request.user.username and not has_role(request.user, 'admin'):
                return Response(
                    {'error': 'Only admins can edit other users.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            user = User.objects.filter(username=username).first()
            if not user:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Validate and save
        serializer = UserSerializer(user, data=request.data, partial=not full_update)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'message': 'User updated successfully.'})


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, username=None):
        # Handle self-deletion
        if not username:
            user = request.user
        else:
            # Reject if not admin and trying to delete others
            if username != request.user.username and not has_role(request.user, 'admin'):
                return Response(
                    {'error': 'Only admins can delete other users.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            user = User.objects.filter(username=username).first()
            if not user:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Prevent superuser deletion
        if user.is_superuser:
            return Response(
                {'error': 'Superuser accounts cannot be deleted via API.'},
                status=status.HTTP_403_FORBIDDEN
            )

        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        # Self profile access
        if not username:
            user = request.user
        else:
            # Prevent unauthorized access to other profiles
            if username != request.user.username and not has_role(request.user, 'admin'):
                return Response(
                    {'error': 'You do not have permission to view other users\' profiles.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            user = User.objects.filter(username=username).first()
            if not user:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

