from django.urls import path

from courses.views import ListCourseView

urlpatterns = [
    path('list-courses/', ListCourseView.as_view(), name='list-courses')
]


