from django.utils import timezone
from xmlrpc.client import DateTime
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsAdmin, IsModerator, IsStudent
from enrollment.serializers import EnrollmentSerializer
from enrollment.models import Enrollment
from icecream import ic
from users.serializers import StudentSerializer
from users.models import Student


class AddEnrollmentView(APIView):
    """
    API endpoint that allows students to create new enrollment requests.

    This view handles POST requests to create new enrollment records.
    Only authenticated students are permitted to access this endpoint.

    Attributes
    ----------
    permission_classes : tuple
        Specifies that only students can access this view (IsStudent).
    queryset : QuerySet
        The base queryset for enrollment objects (all enrollments).
    serializer_class : Serializer
        The serializer class used for enrollment operations.
    """

    permission_classes = (IsStudent,)  # Student can fill up the Enrollment Form
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    @swagger_auto_schema(
        operation_description="Create a new enrollment request",
        operation_summary="Create enrollment",
        responses={
            201: openapi.Response(
                description="Enrollment created successfully",
                schema=EnrollmentSerializer
            ),
            400: "Bad request - invalid data",
            403: "Forbidden - user is not a student"
        },
        tags=['Enrollments'],
        request_body=EnrollmentSerializer
    )
    def post(self, request):

        serializer = EnrollmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            course = serializer.validated_data['course']
            if Enrollment.objects.filter(user=request.user, course=course).exists():
                return Response({'message': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(course = course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListEnrollmentView(ListAPIView):
    """
    API endpoint that lists all enrollment requests.

    This view handles GET requests to retrieve all enrollment records.
    Only admin and moderator users are permitted to access this endpoint.

    Attributes
    ----------
    permission_classes : list
        Specifies that both admins and moderators can access this view.
    queryset : QuerySet
        The base queryset for enrollment objects (all enrollments).
    serializer_class : Serializer
        The serializer class used for enrollment operations.
    """

    permission_classes = [IsAdmin | IsModerator]
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    @swagger_auto_schema(
        operation_description="List all enrollment requests",
        operation_summary="List enrollments",
        responses={
            200: openapi.Response(
                description="List of all enrollments",
                schema=EnrollmentSerializer(many=True))
        },
        tags=['Enrollments'],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class EditEnrollmentView(UpdateAPIView):
    """
    API endpoint that allows modification of enrollment requests.

    This view handles PATCH requests to update enrollment records.
    Only admin and moderator users are permitted to access this endpoint.
    PUT requests are explicitly disabled (HTTP 405).

    When updating status to 'approved', automatically sets:
    - Enrolled_Date to current time
    - approved_by to current user's role

    Attributes
    ----------
    permission_classes : list
        Specifies that both admins and moderators can access this view.
    queryset : QuerySet
        The base queryset for enrollment objects (all enrollments).
    serializer_class : Serializer
        The serializer class used for enrollment operations.
    lookup_field : str
        The field used for object lookup (default 'id').

    Methods
    -------
    put(request, *args, **kwargs)
        Disables PUT method (returns HTTP 405).
    patch(request, *args, **kwargs)
        Handles partial updates with special logic for status changes.
    """

    permission_classes = [IsAdmin | IsModerator]
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="PUT method not allowed",
        operation_summary="PUT not allowed",
        responses={405: "Method Not Allowed"},
        tags=['Enrollments'],
        auto_schema=None
    )

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests.

        Returns
        -------
        Response
            HTTP 405 Method Not Allowed response as PUT is disabled.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(
        operation_description="Update an enrollment request",
        operation_summary="Update enrollment",
        responses={
            200: openapi.Response(
                description="Enrollment updated successfully",
                schema=EnrollmentSerializer
            ),
            400: "Bad request - invalid data",
            403: "Forbidden - user is not admin/moderator",
            404: "Not found - enrollment does not exist"
        },
        tags=['Enrollments'],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="Enrollment ID",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for partial updates.

        Special handling when status changes to 'approved':
        - Sets Enrolled_Date to current time
        - Sets approved_by to current user's role

        Returns
        -------
        Response
            HTTP 200 with serialized data on success,
            HTTP 400 with errors if validation fails.
        """
        enrollment = self.get_object()
        serializer = self.get_serializer(
            enrollment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            # Check if status is becoming approved
            new_status = serializer.validated_data.get("status")
            new_payment = serializer.validated_data.get("payment")
            if (new_status == "approved" and enrollment.status != "approved") and (new_payment == "paid" and enrollment.payment != "paid" ) :
                approver = self.request.user
                serializer.save(
                    Enrolled_Date=timezone.now(),
                    approved_by= f'{approver.username} ({approver.role})'    # i.e. Either 'admin' or 'moderator' in a role and their respective username.
                )

                try:
                    student = Student.objects.get(user__username=enrollment.user)
                    student.is_approved = True
                    student.save()

                except Student.DoesNotExist:

                    return Response({"message" : "Student Not Found"},status=status.HTTP_404_NOT_FOUND)

                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                serializer.save()
                return Response({"message" : "Enrollment already approved"},status=status.HTTP_400_BAD_REQUEST)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEnrollmentView(DestroyAPIView):
    """
    API endpoint that allows deletion of enrollment requests.

    This view handles DELETE requests to remove enrollment records.
    Only admin users are permitted to access this endpoint.

    Attributes
    ----------
    permission_classes : tuple
        Specifies that only admins can access this view (IsAdmin).
    queryset : QuerySet
        The base queryset for enrollment objects (all enrollments).
    serializer_class : Serializer
        The serializer class used for enrollment operations.
    lookup_field : str
        The field used for object lookup (default 'id').
    """

    permission_classes = (IsAdmin,)
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Delete an enrollment request",
        operation_summary="Delete enrollment",
        responses={
            204: "No content - successfully deleted",
            403: "Forbidden - user is not admin",
            404: "Not found - enrollment does not exist"
        },
        tags=['Enrollments'],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="Enrollment ID",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)