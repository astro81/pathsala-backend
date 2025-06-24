from django.urls import path

from courses.views import ListCourseView, AddCourseView

urlpatterns = [
    path('list-courses/', ListCourseView.as_view(), name='list-courses'),
    path('add-course/', AddCourseView.as_view(), name='add-course'),
]


