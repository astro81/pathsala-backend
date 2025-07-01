from django.utils import timezone
from xmlrpc.client import DateTime

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsAdmin , IsModerator , IsStudent
from enrollment.serializers import EnrollmentSerializer
from enrollment.models import Enrollment
from datetime import datetime
# Create your views here.

class AddEnrollmentView(CreateAPIView):

    permission_classes = (IsStudent,)  #todo: Student can fill up the Enrollment Form.......
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class ListEnrollmentView(ListAPIView):

    permission_classes = [IsAdmin | IsModerator]
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class EditEnrollmentView(UpdateAPIView):

    permission_classes = [IsAdmin | IsModerator]
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        enrollment = self.get_object()
        serializer = self.get_serializer(enrollment, data=request.data, partial=True)

        if serializer.is_valid():
            # Check if status is becoming approved
            new_status = serializer.validated_data.get("status") # Field which is used while updating through patch.
            if new_status == "approved" and enrollment.status != "approved":
                serializer.save(Enrolled_Date=timezone.now(), approved_by=self.request.user.role)

            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEnrollmentView(DestroyAPIView):

    permission_classes = (IsAdmin,)
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    lookup_field = 'id'
