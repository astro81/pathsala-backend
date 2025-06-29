from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rolepermissions.roles import remove_role, assign_role

from users.models import Student, Moderator
from users.permissions import IsAdmin, IsStudent, IsModerator
from users.serializers import StudentSerializer, UserSerializer, ModeratorSerializer


from icecream import ic

User = get_user_model()


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username:
                raise ValidationError({"error": "Username is required"})
            if not password:
                raise ValidationError({"error": "Password is required"})

            user = authenticate(username=username, password=password)

            if not user:
                raise ValidationError({"error": "Invalid credentials"})

            if not user.is_active:
                return Response({"error": "User is inactive"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            if not tokens.exists():
                return Response({"message": "No active tokens found"}, status=status.HTTP_200_OK)

            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response({"message": "Successfully logged out from all devices"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


########################
# *Registration views* #
########################
class StudentRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = StudentSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Student created successfully"}, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "Database integrity error occurred"}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({"error": "Database operation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModeratorRegisterView(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request):
        try:
            serializer = ModeratorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({"message": "Moderator created successfully"}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "Database integrity error occurred"}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({"error": "Database operation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###################
# *Profile views* #
###################
class UserOwnProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            serialized_user = UserSerializer(user).data

            # Add student-specific data if the user is a student
            if user.role == user.Role.STUDENT:
                try:
                    student = Student.objects.get(user=user)
                    profile_data = {
                        "address": student.address,
                        "phone_no": student.phone_no,
                        "is_approved": student.is_approved
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
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AdminUserDetailView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, username):
        try:
            user = get_object_or_404(User, username=username)
            data = UserSerializer(user).data

            if user.role == user.Role.STUDENT:
                try:
                    student = Student.objects.get(user=user)
                    profile_data = {
                        "address": student.address,
                        "phone_no": student.phone_no,
                        "is_approved": student.is_approved
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
                data.update({
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role
                })

            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


##################
# *Update views* #
##################
class StudentProfileUpdateView(APIView):
    permission_classes = (IsStudent,)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request):
        try:
            user = request.user
            student = Student.objects.get(user=user)
            
            serializer = StudentSerializer(
                student, 
                data=request.data, 
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({"message": "Profile successfully updated!"}, status=status.HTTP_200_OK)
            
        except ObjectDoesNotExist:
            return Response({"message": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModeratorProfileUpdateView(APIView):
    permission_classes = (IsModerator,)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request):
        try:
            user = request.user
            moderator = Moderator.objects.get(user=user)
            
            serializer = ModeratorSerializer(
                moderator, 
                data=request.data, 
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(
                {"message": "Profile successfully updated!"},
                status=status.HTTP_200_OK
            )
            
        except ObjectDoesNotExist:
            return Response({"message": "Moderator profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
#################
# *Delete view* #
#################
def delete_token_helper(user):
    for token in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=token)

def delete_user_role_helper(user):
    if user.role == User.Role.STUDENT:
        remove_role(user, 'student')
    if user.role == User.Role.MODERATOR:
        remove_role(user, 'moderator')


# todo: take username and confirm the user is valid to ensure integrity
class UserDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            user = request.user
            username = request.get.get('username')
            password = request.get.get('password')

            if not username:
                return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
            if not password:
                return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

            if user.username != username:
                return Response({"error": "Username does not matches the logged in user"}, status=status.HTTP_400_BAD_REQUEST)

            authenticated_user = authenticate(username=username, password=password)
            if (not authenticated_user) or (authenticated_user != user):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if user.role not in [User.Role.MODERATOR, User.Role.STUDENT]:
                return Response({"message": "Only moderators and students can delete their account"}, status=status.HTTP_403_FORBIDDEN)

            delete_token_helper(user)
            delete_user_role_helper(user)

            user.is_active = False
            user.save()

            return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminDeleteUserView(APIView):
    permission_classes = (IsAdmin,)
    permanently_delete: bool = False

    def delete(self, request, user_id):
        try:
            admin = request.user
            user = get_object_or_404(User, pk=user_id)

            # Get confirmation username from request data
            confirm_username = request.data.get('username')

            # Validate confirmation username
            if not confirm_username:
                return Response({"error": "Please provide the username of the user you want to delete as confirmation"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify username matches the user being deleted
            if confirm_username != user.username:
                return Response({"error": "Confirmation username does not match the user you're trying to delete"}, status=status.HTTP_400_BAD_REQUEST)

            # Prevent deletion of the admin account
            if user.id == admin.id:
                return Response({"message": "You cannot delete the admin account"}, status=status.HTTP_403_FORBIDDEN)

            delete_token_helper(user)
            delete_user_role_helper(user)

            if self.permanently_delete:                 #! Permanently delete the user
                user.delete()
                message = "User permanently deleted!"
            else:                                       #! Soft delete the user by setting is_active to False
                user.is_active = False
                user.save()
                message = "User deactivated successfully!"

            return Response({"message": message}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReactivateUserView(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request, user_id):
        try:
            # Get the inactive user
            user = get_object_or_404(User, pk=user_id, is_active=False)

            # Reactivate the account
            user.is_active = True
            user.save()

            # Restore the appropriate role based on the user's role field
            if user.role == User.Role.MODERATOR:
                assign_role(user, 'moderator')
            if user.role == User.Role.STUDENT:
                assign_role(user, 'student')

            return Response(
                {"message": "Account reactivated successfully with original role"},
                status=status.HTTP_200_OK
            )

        except ObjectDoesNotExist:
            return Response({"message": "Inactive user not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserFilter(filters.FilterSet):
    """
    Filter set for the User model with various filtering options.
    """
    role = filters.ChoiceFilter(choices=User.Role.choices)
    is_active = filters.BooleanFilter()
    is_staff = filters.BooleanFilter()
    is_superuser = filters.BooleanFilter()

    # Date filters
    date_joined = filters.DateFromToRangeFilter()
    last_login = filters.DateFromToRangeFilter()

    # Text-based filters
    username = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')

    # Multiple choice filters
    roles = filters.MultipleChoiceFilter(
        field_name='role',
        choices=User.Role.choices
    )

    class Meta:
        model = User
        fields = [
            'role', 'roles', 'is_active', 'is_staff', 'is_superuser',
            'username', 'email', 'first_name', 'last_name',
            'date_joined', 'last_login'
        ]


class UserListAPIView(ListAPIView):
    """
    API view to list all users - accessible only by admins.

    Supports filtering, searching, and ordering:
    - Filter by role, active status, staff status, etc.
    - Search by username, email, first_name, last_name
    - Order by any field (use - prefix for descending order)

    Example URLs:
    - /api/users/                                    # List all users
    - /api/users/?role=student                       # Filter by role
    - /api/users/?roles=student,moderator            # Filter by multiple roles
    - /api/users/?is_active=true                     # Filter by active status
    - /api/users/?search=john                        # Search across username, email, names
    - /api/users/?ordering=-date_joined              # Order by date joined (newest first)
    - /api/users/?username__icontains=admin          # Filter usernames containing 'admin'
    - /api/users/?date_joined__gte=2024-01-01        # Users joined after date
    """

    queryset = User.objects.all().select_related().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    # Backend filters
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Django filter configuration
    filterset_class = UserFilter

    # Search configuration
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name'
    ]

    # Ordering configuration
    ordering_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'date_joined',
        'last_login'
    ]

    ordering = ['-date_joined']  # Default ordering

    def get_queryset(self):
        """
        Optionally restricts the returned users based on query parameters.
        """
        queryset = super().get_queryset()

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Override the list method to add custom response formatting if needed.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return Response({
                'success': True,
                'count': queryset.count(),
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'error': 'Failed to retrieve users',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


