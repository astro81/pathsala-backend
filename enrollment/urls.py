from django.urls import path
from enrollment.views import AddEnrollmentView, ListEnrollmentView, DeleteEnrollmentView

urlpatterns = [

    path('addenrollment/', AddEnrollmentView.as_view(), name='add-enrollment'),
    path('listenrollment/', ListEnrollmentView.as_view(), name='list-enrollment'),
    path('deleteenrollment/', DeleteEnrollmentView.as_view(), name='delete-enrollment'),
]