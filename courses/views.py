from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from courses.models import Course
from courses.serializers import CourseSerializer
from users.permissions import HasCoursePermission


# Create your views here.
class ListCourseView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = {
        'training_level': ['exact'],
        'class_type': ['exact'],
        'price': ['gte', 'lte'],
        'rating': ['gte', 'lte'],
        'duration': ['gte', 'lte'],
    }

    search_fields = ['name', 'title', 'career_prospect']

    ordering_fields = ['name', 'price', 'rating', 'duration', 'created_at']
    ordering = ['-created_at']  # Default ordering (newest first)

    def handle_exception(self, exc):
        if isinstance(exc, Course.DoesNotExist):
            return Response(
                {"error": "No courses found matching the criteria."},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().handle_exception(exc)


class AddCourseView(CreateAPIView):
    permission_classes = [HasCoursePermission]
    required_permission = 'add_course'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
            return Response({"message": "Course Added Successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to add course: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)




