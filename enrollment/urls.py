from django.urls import path
from enrollment.views import (
    AddEnrollmentView,
    ListEnrollmentView,
    DeleteEnrollmentView,
    EditEnrollmentView
)

"""
    URL patterns for enrollment-related operations.

    This module defines the URL routing for all enrollment operations including:
    - Creating new enrollments
    - Listing existing enrollments
    - Editing enrollment records
    - Deleting enrollments

    Patterns
    --------
    addenrollment/ : AddEnrollmentView
        Endpoint for creating new enrollment records.
    listenrollment/ : ListEnrollmentView
        Endpoint for listing all enrollment records.
    editenrollment/<str:id>/ : EditEnrollmentView
        Endpoint for modifying specific enrollment records.
    deleteenrollment/<str:id>/ : DeleteEnrollmentView
        Endpoint for deleting specific enrollment records.

    Notes
    -----
    All URLs are prefixed with the application's base URL.
    The <str:id> parameter represents the UUID of the enrollment record.
"""
urlpatterns = [

    path('addenrollment/', AddEnrollmentView.as_view(), name='add-enrollment'),
    path('listenrollment/', ListEnrollmentView.as_view(), name='list-enrollment'),
    path('editenrollment/<str:id>/', EditEnrollmentView.as_view(), name='edit-enrollment'),
    path('deleteenrollment/<str:id>/', DeleteEnrollmentView.as_view(), name='delete-enrollment'),
]