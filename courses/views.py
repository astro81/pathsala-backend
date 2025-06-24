from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from courses.models import Course
from courses.serializers import CourseSerializer


# Create your views here.
class ListCourseView(ListAPIView):
    permission_classes = AllowAny,
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


