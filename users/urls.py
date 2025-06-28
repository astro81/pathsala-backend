from django.urls import path

from users.views import (
    LoginView, LogoutView, LogoutAllView,
    StudentRegisterView, ModeratorRegisterView,
    UserOwnProfileView, AdminUserDetailView,
    StudentProfileUpdateView, ModeratorProfileUpdateView,
    UserDeleteView, AdminDeleteUserView, ReactivateUserView, UserListAPIView)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),

    path('register/student/', StudentRegisterView.as_view(), name='student-register'),
    path('register/moderator/', ModeratorRegisterView.as_view(), name='moderator-register'),

    path('user/profile/', UserOwnProfileView.as_view(), name='user-profile'),
    path('admin/profile/<str:username>/', AdminUserDetailView.as_view(), name='admin-profile'),

    path('update/student/profile/', StudentProfileUpdateView.as_view(), name='update-student-profile'),
    path('update/moderator/profile/', ModeratorProfileUpdateView.as_view(), name='update-moderator-profile'),

    path('user/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('admin/delete/temporary/<str:user_id>/', AdminDeleteUserView.as_view(permanently_delete = False), name='admin-soft-delete-user'),
    path('admin/delete/permanent/<str:user_id>/', AdminDeleteUserView.as_view(permanently_delete=True), name='admin-hard-delete-user'),

    path('admin/reactivate/<str:user_id>/', ReactivateUserView.as_view(), name='admin-reactivate'),

    path('users/', UserListAPIView.as_view(), name='user-list'),
]

