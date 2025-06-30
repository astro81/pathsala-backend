"""URL configuration for category management API endpoints.

This module defines the routing for all category-related operations including:
- Category creation
- Category listing
- Category retrieval
- Category updates
- Category deletion

All endpoints follow RESTful conventions and use appropriate HTTP methods.
"""

from django.urls import path
from category.views import (
    AddCategoryView,
    ListCategoryView,
    EditCategoryView,
    ViewCategory,
    DeleteCategoryView
)


app_name = 'category'

urlpatterns = [

    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('list-category/', ListCategoryView.as_view(), name='list_category'),
    path('edit-category/<str:name>/', EditCategoryView.as_view(), name='edit_category'),
    path('view-category/<str:name>/', ViewCategory.as_view(), name='view_category'),
    path('delete-category/<str:name>/', DeleteCategoryView.as_view(), name='delete_category'),
]