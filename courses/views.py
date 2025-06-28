from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from courses.models import Course
from courses.serializers import CourseSerializer
from courses.permissions import HasCoursePermission


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
        'duration_value': ['gte', 'lte'],
    }

    search_fields = ['name', 'title', 'career_prospect']

    ordering_fields = ['name', 'price', 'rating', 'duration_value', 'created_at']
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




class ViewCourse(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'name' # looks or wait for a name in the url for filtering the retrieving course

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)



class EditCourseView(UpdateAPIView):
    permission_classes = [HasCoursePermission]
    required_permission = 'edit_course'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'name'

    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteCourseView(DestroyAPIView):
    permission_classes = [HasCoursePermission]
    required_permission = 'delete_course'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'name'

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        self.perform_destroy(course)
        return Response({"message": "Course Deleted Successfully!"}, status=status.HTTP_200_OK)


