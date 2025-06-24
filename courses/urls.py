from django.urls import path

from courses.views import ListCourseView, AddCourseView, ViewCourse, EditCourseView, DeleteCourseView

urlpatterns = [
    path('list-courses/', ListCourseView.as_view(), name='list-courses'),
    path('add-course/', AddCourseView.as_view(), name='add-course'),
    path('view-course/<str:name>/', ViewCourse.as_view(), name='view-course'),
    path('edit-course/<str:name>/', EditCourseView.as_view(), name='edit-course'),
    path('delete-course/<str:name>/', DeleteCourseView.as_view(), name='delete-course'),
]


