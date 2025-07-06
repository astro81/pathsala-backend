"""Views for the course management system.

This module contains all API endpoints for course operations including:
- Course creation
- Course listing and filtering
- Course retrieval
- Course updates
- Course deletion
- Featured courses listing
"""
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
    ParseError
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from courses.models import Course
from courses.permissions import HasCoursePermission
from courses.serializers import CourseSerializer, CourseListSerializer, CourseImageSerializer


class CreateCourseView(CreateAPIView):
    """API endpoint for creating new courses.

    Attributes
    ----------
    permission_classes : tuple
        Custom permission class that checks for 'add_course' permission
    required_permission : str
        The specific permission string required
    queryset : QuerySet
        Base queryset for course objects
    serializer_class : Serializer
        Serializer class for course data
    """

    permission_classes = (HasCoursePermission,)
    required_permission = 'add_course'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: "Bad Request - Invalid input data",
            403: "Forbidden - User lacks required permissions",
            500: "Internal Server Error"
        },
        tags=['Courses'],
        security=[{'Bearer': []}]
    )
    def create(self, request, *args, **kwargs):
        """Handle course creation with proper error responses.

        Parameters
        ----------
        request : Request
            The incoming HTTP request
        *args : tuple
            Additional positional arguments
        **kwargs : dict
            Additional keyword arguments

        Returns
        -------
        Response
            HTTP response with created course data or error message

        Raises
        ------
        ValidationError
            If input data is invalid
        PermissionDenied
            If the user lacks required permissions
        Exception
            For any unexpected errors
        """
        try:
            return super().create(request, *args, **kwargs)
        except (ValidationError, ParseError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {'error': f"Failed to create course: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        """Set the course owner to the current user during creation.

        Parameters
        ----------
        serializer : CourseSerializer
            The serializer instance with validated data
        """
        serializer.save(owner=self.request.user)


class CourseFilter(filters.FilterSet):
    average_rating = filters.NumberFilter(method='filter_average_rating')
    average_rating__gte = filters.NumberFilter(method='filter_average_rating_gte')
    average_rating__lte = filters.NumberFilter(method='filter_average_rating_lte')

    def filter_average_rating(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating=value)

    def filter_average_rating_gte(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating__gte=value)

    def filter_average_rating_lte(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating__lte=value)

    class Meta:
        model = Course
        fields = {
            'training_level': ['exact'],
            'class_type': ['exact'],
            'duration_weeks': ['exact', 'gte', 'lte'],
            'price': ['exact', 'gte', 'lte'],
            'title': ['exact', 'icontains'],
            'categories__name': ['exact', 'icontains'],
        }

class ListCourseView(ListAPIView):
    """API endpoint for listing and filtering courses."""

    permission_classes = (AllowAny,)
    serializer_class = CourseListSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter

    search_fields = ['name', 'title', 'overview', 'categories__name']

    ordering_fields = [
        'name',
        'title',
        'price',
        'duration_weeks',
        'created_at',
        'avg_rating',  # Changed from average_rating to avg_rating
    ]

    ordering = ['-created_at']

    def get_queryset(self):
        """Annotate the queryset with avg_rating for ordering."""
        return Course.objects.annotate(
            avg_rating=Avg('ratings__rating')
        ).all()


class RetrieveCourseView(RetrieveAPIView):
    """API endpoint for retrieving a single course by name.

    Attributes
    ----------
    permission_classes : tuple
        Permission settings (AllowAny for retrieval)
    serializer_class : Serializer
        Serializer for course data
    queryset : QuerySet
        Base queryset of all courses
    lookup_field : str
        Field to use for object lookup (name)
    """

    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = 'name'

    @swagger_auto_schema(
        operation_description="Retrieve a specific course by its name",
        responses={
            200: CourseSerializer,
            404: "Not Found - Course not found",
            500: "Internal Server Error"
        },
        tags=['Courses']
    )
    def retrieve(self, request, *args, **kwargs):
        """Handle course retrieval with error handling.

        Parameters
        ----------
        request : Request
            The incoming HTTP request
        *args : tuple
            Additional positional arguments
        **kwargs : dict
            Additional keyword arguments

        Returns
        -------
        Response
            HTTP response with course data or error message
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f"Error retrieving course: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EditCourseView(UpdateAPIView):
    """API endpoint for updating existing courses.

    Attributes
    ----------
    permission_classes : tuple
        Custom permission class that checks for 'edit_course' permission
    required_permission : str
        The specific permission string required
    serializer_class : Serializer
        Serializer for course data
    queryset : QuerySet
        Base queryset of all courses
    lookup_field : str
        Field to use for object lookup (name)
    """

    permission_classes = (HasCoursePermission,)
    required_permission = 'edit_course'
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = 'name'

    @swagger_auto_schema(
        operation_description="Update an existing course",
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: "Bad Request - Invalid input data",
            403: "Forbidden - User lacks required permissions",
            404: "Not Found - Course not found",
            500: "Internal Server Error"
        },
        tags=['Courses'],
        security=[{'Bearer': []}]
    )
    def update(self, request, *args, **kwargs):
        """Handle course updates with proper error responses.

        Parameters
        ----------
        request : Request
            The incoming HTTP request
        *args : tuple
            Additional positional arguments
        **kwargs : dict
            Additional keyword arguments

        Returns
        -------
        Response
            HTTP response with updated course data or error message
        """
        try:
            return super().update(request, *args, **kwargs)
        except (ValidationError, ParseError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f"Failed to update course: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_update(self, serializer):
        """Set the updated_by field to current user during update.

        Parameters
        ----------
        serializer : CourseSerializer
            The serializer instance with validated data
        """
        serializer.save(updated_by=self.request.user)


class DeleteCourseView(DestroyAPIView):
    """API endpoint for deleting courses.

    Attributes
    ----------
    permission_classes : tuple
        Custom permission class that checks for 'delete_course' permission
    required_permission : str
        The specific permission string required
    serializer_class : Serializer
        Serializer for course data
    queryset : QuerySet
        Base queryset of all courses
    lookup_field : str
        Field to use for object lookup (name)
    """

    permission_classes = (HasCoursePermission,)
    required_permission = 'delete_course'
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = 'name'

    @swagger_auto_schema(
        operation_description="Delete a course",
        responses={
            204: "No Content - Successfully deleted",
            400: "Bad Request - Invalid parameters",
            403: "Forbidden - User lacks required permissions",
            404: "Not Found - Course not found",
            500: "Internal Server Error"
        },
        tags=['Courses'],
        security=[{'Bearer': []}]
    )
    def destroy(self, request, *args, **kwargs):
        """Handle course deletion with proper error responses.

        Parameters
        ----------
        request : Request
            The incoming HTTP request
        *args : tuple
            Additional positional arguments
        **kwargs : dict
            Additional keyword arguments

        Returns
        -------
        Response
            HTTP response with a success/error message
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except (ValidationError, ParseError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f"Failed to delete course: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CourseFeaturedListView(ListAPIView):
    """API endpoint that returns featured courses (highest rated).

    Featured courses are defined as those with average rating >= 4.0,
    ordered by rating (highest first), limited to 5 results.

    Attributes
    ----------
    permission_classes : tuple
        Permission settings (AllowAny for listing)
    serializer_class : Serializer
        Serializer for course data
    """

    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_description="Get featured courses (highest rated, rating >= 4.0, limited to 5 results)",
        responses={
            200: CourseSerializer(many=True),
            500: "Internal Server Error"
        },
        tags=['Courses']
    )
    def list(self, request, *args, **kwargs):
        """Retrieve and return featured courses with error handling.

        Parameters
        ----------
        request : Request
            The incoming HTTP request
        *args : tuple
            Additional positional arguments
        **kwargs : dict
            Additional keyword arguments

        Returns
        -------
        Response
            HTTP response with a featured courses list or error message
        """
        try:
            from django.db.models import Avg
            self.queryset = Course.objects.annotate(
                average_rating=Avg('ratings__rating')
            ).filter(average_rating__gte=4.0).order_by('-average_rating')[:5]
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': f"Error retrieving featured courses: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateCourseImageView(UpdateAPIView):
    """API endpoint specifically for updating course images."""

    permission_classes = (HasCoursePermission,)
    required_permission = 'edit_course'
    parser_classes = [MultiPartParser]  # Only accept multipart/form-data
    serializer_class = CourseImageSerializer
    queryset = Course.objects.all()
    lookup_field = 'name'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({
                'status': 'success',
                'message': 'Image updated successfully',
                'image_url': instance.image.url if instance.image else None
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied:
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {'error': f"Failed to update image: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
