from django.urls import path
from .views import (
    RegisterUserView, LoginUserView, LogoutUserView, RefreshTokenView,
    CreateModeratorView, EditUserView, DeleteUserView,
    ReactivateUserView, UserProfileView, UserListView
)

app_name = 'users'


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    path('create-moderator/', CreateModeratorView.as_view(), name='create_moderator'),

    path('user/edit/', EditUserView.as_view(), name='edit_self'),
    path('user/edit/<str:username>/', EditUserView.as_view(), name='edit_user_by_admin'),

    path('user/delete/', DeleteUserView.as_view(), name='delete_self'),
    path('user/delete/<str:username>/', DeleteUserView.as_view(), name='delete_user_by_admin'),

    path('user/reactivate/<str:username>/', ReactivateUserView.as_view(), name='reactivate_user'),

    path('user/profile/', UserProfileView.as_view(), name='profile_self'),
    path('user/profile/<str:username>/', UserProfileView.as_view(), name='profile_by_username'),

    path('user/list/', UserListView.as_view(), name='user_list'),
]
