
"""URL configuration for courses application.

Defines all the API endpoints related to course management including:
- Course creation
- Course listing
- Course retrieval
- Course modification
- Course deletion
- Featured courses listing
"""

from django.urls import path
from courses.views import (
    CreateCourseView,
    ListCourseView,
    RetrieveCourseView,
    EditCourseView,
    DeleteCourseView,
    CourseFeaturedListView
)

app_name = 'courses'


urlpatterns = [
    path('add/', CreateCourseView.as_view(), name='add_course'),
    path('list/', ListCourseView.as_view(), name='list_course'),
    path('<str:name>/', RetrieveCourseView.as_view(), name='view_course'),
    path('update/<str:name>/', EditCourseView.as_view(), name='update_course'),
    path('delete/<str:name>/', DeleteCourseView.as_view(), name='delete_course'),
    path('featured/', CourseFeaturedListView.as_view(), name='featured_course'),
]

