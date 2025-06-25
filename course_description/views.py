from django.shortcuts import render
from rest_framework import viewsets

from course_description.models import CourseDescription


# Create your views here.
class CourseDescriptionViewSet(viewsets.ModelViewSet):
    queryset = CourseDescription.objects.all()
    serializer_class = CourseDescription