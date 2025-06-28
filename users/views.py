from django.contrib.auth import authenticate, get_user_model
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
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


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)

        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response({"message": "Successfully logged out from all devices"}, status=status.HTTP_205_RESET_CONTENT)


####################
# *Register views* #
####################
class StudentRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeratorRegisterView(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = ModeratorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Moderator created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###################
# *Profile views* #
###################
class UserOwnProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        # Start with core user data from a serializer
        serialized_user = UserSerializer(user).data

        # Add student-specific data if the user is a student
        if user.role == user.Role.STUDENT:
            try:
                student = Student.objects.get(user=user)
                serialized_user.update({
                    "address": student.address,
                    "phone_no": student.phone_no,
                    "profile_picture": request.build_absolute_uri(student.profile_picture.url)
                        if student.profile_picture else None,
                    "is_approved": student.is_approved
                })
            except Student.DoesNotExist:
                pass

        # todo: add moderator-specific data if the user is a moderator

        return Response(serialized_user, status=status.HTTP_200_OK)


class AdminUserDetailView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        data = UserSerializer(user).data

        if user.role == user.Role.STUDENT:
            try:
                student = Student.objects.get(user=user)
                data.update({
                    "address": student.address,
                    "phone_no": student.phone_no,
                    "profile_picture": request.build_absolute_uri(student.profile_picture.url) if student.profile_picture else None,
                    "is_approved": student.is_approved,
                })
            except Student.DoesNotExist:
                pass
        else:
            data.update({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role
            })

        return Response(data, status=status.HTTP_200_OK)


##################
# *Update views* #
##################
class StudentProfileUpdateView(APIView):
    permission_classes = (IsStudent,)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request):
        user = request.user

        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"message": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile successfully updated!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeratorProfileUpdateView(APIView):
    permission_classes = (IsModerator,)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request):
        user = request.user

        try:
            moderator = Moderator.objects.get(user=user)
        except Moderator.DoesNotExist:
            return Response({"message": "Moderator profile not found"},
                          status=status.HTTP_404_NOT_FOUND)

        serializer = ModeratorSerializer(moderator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile successfully updated!"},
                          status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        user = request.user

        if user.role not in [User.Role.MODERATOR, User.Role.STUDENT]:
            return Response({"message": "Only moderators and students can delete their account"}, status=status.HTTP_403_FORBIDDEN)

        try:
            delete_token_helper(user)
            delete_user_role_helper(user)

            # Soft delete the user by setting is_active to False
            user.is_active = False
            user.save()

            return Response(
                {"message": "Account deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminDeleteUserView(APIView):
    permission_classes = (IsAdmin,)

    permanently_delete: bool = False

    def delete(self, request, user_id):
        admin = request.user

        try:
            user = get_object_or_404(User, pk=user_id)

            # Prevent deletion of the admin account
            if user.id == admin.id:
                return Response({"message": "You cannot delete the admin account"}, status=status.HTTP_403_FORBIDDEN)

            delete_token_helper(user)
            delete_user_role_helper(user)

            if self.permanently_delete:                 #! Permanently delete the user
                user.delete()
            else:                                       #! Soft delete the user by setting is_active to False
                user.is_active = False
                user.save()

            return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)
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

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# todo: list users by admin
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


