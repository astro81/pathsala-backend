from django.urls import path
from enrollment.views import AddEnrollmentView, ListEnrollmentView, DeleteEnrollmentView, EditEnrollmentView

urlpatterns = [

    path('addenrollment/', AddEnrollmentView.as_view(), name='add-enrollment'),
    path('listenrollment/', ListEnrollmentView.as_view(), name='list-enrollment'),
    path('editenrollment/<str:id>/', EditEnrollmentView.as_view(), name='edit-enrollment'),
    path('deleteenrollment/<str:id>/', DeleteEnrollmentView.as_view(), name='delete-enrollment'),
]