"""URL configuration for course ratings API endpoints.

This module defines the following endpoints:
- Course rating submission (create/update)
- Course rating retrieval (single user)
- Course ratings listing (all users)

All endpoints require course_id as a UUID parameter in the URL.
"""

from django.urls import path
from course_ratings.views import (
    AddCourseRatingView,
    CheckCourseRatingView,
    CourseRatingListView
)


app_name = 'course_ratings'

urlpatterns = [
    path('rate/<uuid:course_id>/', AddCourseRatingView.as_view(), name='add_course_rating'),

    path('check/<uuid:course_id>/', CheckCourseRatingView.as_view(), name='check_course_rating'),

    path('list/<uuid:course_id>/', CourseRatingListView.as_view(), name='course_rating_list')
]
