"""Views for the course rating system.

This module contains API endpoints for:
- Adding/updating course ratings
- Checking existing ratings
- Listing all ratings for a course
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_role

from course_ratings.models import CourseRating
from course_ratings.serializers import CourseRatingSerializer
from courses.models import Course
from courses.permissions import HasCoursePermission
from users.permissions import IsStudent


class AddCourseRatingView(APIView):
    """API endpoint for adding or updating course ratings.

    Permissions:
    - Requires 'rate_course' permission
    - Only accessible to students

    Methods:
    - post: Create or update a course rating
    """

    permission_classes = [IsStudent]
    # permission_classes = [HasCoursePermission]
    # required_permission = 'rate_course'

    @swagger_auto_schema(
        operation_description="Add or update a course rating (students only)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['rating'],
            properties={
                'rating': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Rating value (1-5)",
                    minimum=1,
                    maximum=5
                ),
                'review': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Optional review text",
                    maxLength=500
                )
            }
        ),
        responses={
            201: CourseRatingSerializer,
            200: CourseRatingSerializer,
            400: "Bad Request - Invalid input data",
            403: "Forbidden - User is not a student or lacks permission",
            404: "Not Found - Course not found",
            500: "Internal Server Error"
        },
        tags=['Course Ratings'],
        security=[{'Bearer': []}]
    )
    def post(self, request, course_id):
        """Create or update a course rating.

        Parameters:
        - request: HTTP request object
        - course_id: ID of the course to rate

        Returns:
        - 201 Created: When a new rating is created
        - 200 OK: When existing rating is updated
        - 400 Bad Request: For invalid data
        - 403 Forbidden: For non-student users
        - 404 Not Found: If course doesn't exist
        - 500 Internal Server Error: For unexpected errors
        """
        try:
            # Get course with error handling
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response(
                    {"error": "Course not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if the user is a student
            if not has_role(request.user, 'student'):
                return Response(
                    {"error": "Only students can rate courses."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Validate and process rating
            serializer = CourseRatingSerializer(
                data=request.data,
                context={'request': request}
            )
            if not serializer.is_valid():
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update a rating
            rating, created = CourseRating.objects.update_or_create(
                course=course,
                user=request.user,
                defaults=serializer.validated_data
            )

            return Response(
                CourseRatingSerializer(rating).data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to process rating: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CheckCourseRatingView(APIView):
    """API endpoint for checking a user's existing course rating.

    Permissions:
    - Requires 'rate_course' permission

    Methods:
    - get: Retrieve the user's rating for a course
    """

    permission_classes = [HasCoursePermission]
    required_permission = 'rate_course'

    @swagger_auto_schema(
        operation_description="Check the authenticated user's rating for a course",
        responses={
            200: CourseRatingSerializer,
            404: "Not Found - Course or rating not found",
            500: "Internal Server Error"
        },
        tags=['Course Ratings'],
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_PATH,
                description="ID of the course to check",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, course_id):
        """Retrieve the authenticated user's rating for a course.

        Parameters:
        - request: HTTP request object
        - course_id: ID of the course to check

        Returns:
        - 200 OK: With rating data if exists
        - 404 Not Found: If course or rating doesn't exist
        - 500 Internal Server Error: For unexpected errors
        """
        try:
            # Get course with error handling
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response(
                    {"error": "Course not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get user's rating
            try:
                rating = CourseRating.objects.get(
                    course=course,
                    user=request.user
                )
                return Response(CourseRatingSerializer(rating).data)
            except CourseRating.DoesNotExist:
                return Response(
                    {"error": "You haven't rated this course yet."},
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to check rating: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CourseRatingListView(ListAPIView):
    """API endpoint for listing all ratings for a course.

    Permissions:
    - Accessible to any user (AllowAny)

    Methods:
    - get: Retrieve all ratings for a course
    """

    permission_classes = [AllowAny]
    serializer_class = CourseRatingSerializer

    @swagger_auto_schema(
        operation_description="List all ratings for a specific course",
        responses={
            200: CourseRatingSerializer(many=True),
            500: "Internal Server Error"
        },
        tags=['Course Ratings'],
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_PATH,
                description="ID of the course to get ratings for",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Field to order results by (e.g., '-created_at' for newest first)",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        """Retrieve all ratings for a specific course.

        Parameters:
        - request: HTTP request object
        - course_id: ID of the course (from URL)

        Returns:
        - 200 OK: With the list of ratings
        - 500 Internal Server Error: For unexpected errors
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve ratings: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_queryset(self):
        """Get the queryset of ratings for the specified course.

        Returns:
        - QuerySet: Filtered by course_id, with user data prefetched
        """
        course_id = self.kwargs['course_id']
        return CourseRating.objects.filter(
            course_id=course_id
        ).select_related('user')

