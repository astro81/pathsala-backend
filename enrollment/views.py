from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin , IsModerator , IsStudent
from enrollment.serializers import EnrollmentSerializer
from enrollment.models import Enrollment

# Create your views here.

class AddEnrollmentView(CreateAPIView):

    Permission_classes = (IsAuthenticated, IsStudent)   #todo: Student can fill up the Enrollment Form.......
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer



class ListEnrollmentView(ListAPIView):

    Permission_classes = (IsAdmin, IsModerator)
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class DeleteEnrollmentView(DestroyAPIView):

    Permission_classes = (IsAdmin,)
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
