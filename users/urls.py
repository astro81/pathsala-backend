"""
User Management URL Configuration

This module defines all URL routes for user management operations.
The routes are organized by functionality and follow RESTful conventions.

All URLs are prefixed with:
- /api/auth/ (if included in the main project's urls.py)
- Or whatever prefix is defined in the project's URL configuration

"""

from django.urls import path

from users.views import (
    LoginView,
    LogoutView,
    LogoutAllView,
    StudentRegisterView,
    ModeratorRegisterView,
    UserOwnProfileView,
    AdminUserDetailView,
    StudentProfileUpdateView,
    ModeratorProfileUpdateView,
    UserDeleteView,
    AdminDeleteUserView,
    ReactivateUserView,
    UserListAPIView,
)

app_name = "users"

urlpatterns = [
    # Authentication endpoints
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "logout-all/",
        LogoutAllView.as_view(),
        name="logout-all",
    ),

    # Registration endpoints
    path(
        "register/student/",
        StudentRegisterView.as_view(),
        name="student-register",
    ),
    path(
        "register/moderator/",
        ModeratorRegisterView.as_view(),
        name="moderator-register",
    ),

    # Profile endpoints
    path(
        "user/profile/",
        UserOwnProfileView.as_view(),
        name="user-profile",
    ),
    path(
        "admin/profile/<str:username>/",
        AdminUserDetailView.as_view(),
        name="admin-profile",
    ),

    # Profile update endpoints
    path(
        "update/student/profile/",
        StudentProfileUpdateView.as_view(),
        name="update-student-profile",
    ),
    path(
        "update/moderator/profile/",
        ModeratorProfileUpdateView.as_view(),
        name="update-moderator-profile",
    ),

    # Account deletion endpoints
    path(
        "user/delete/",
        UserDeleteView.as_view(),
        name="user-delete",
    ),
    path(
        "admin/delete/temporary/<str:user_id>/",
        AdminDeleteUserView.as_view(permanently_delete=False),
        name="admin-soft-delete-user",
    ),
    path(
        "admin/delete/permanent/<str:user_id>/",
        AdminDeleteUserView.as_view(permanently_delete=True),
        name="admin-hard-delete-user",
    ),

    # Account reactivation endpoint
    path(
        "admin/reactivate/<str:user_id>/",
        ReactivateUserView.as_view(),
        name="admin-reactivate",
    ),

    # User listing endpoint
    path(
        "users/",
        UserListAPIView.as_view(),
        name="user-list",
    ),
]

