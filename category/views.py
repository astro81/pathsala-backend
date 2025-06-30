"""Views for the category management system.

This module contains API endpoints for all category operations including:
- Category creation
- Category listing
- Category retrieval
- Category updates
- Category deletion
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from courses.permissions import HasCoursePermission
from category.models import Category
from category.serializers import CategorySerializer


class AddCategoryView(CreateAPIView):
    """API endpoint for creating new categories.

    Permissions:
    - Requires 'add_category' permission

    Methods:
    - POST: Create a new category
    """

    permission_classes = [HasCoursePermission]
    required_permission = 'add_category'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description="Create a new category",
        request_body=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: "Bad Request - Invalid input data",
            403: "Forbidden - Missing required permissions",
            500: "Internal Server Error"
        },
        tags=['Categories'],
        security=[{'Bearer': []}]
    )
    def create(self, request, *args, **kwargs):
        """Handle category creation with comprehensive error responses.

        Returns:
        --------
        Response
            HTTP response with created category data or error message

        Possible Status Codes:
        - 201 Created: Successfully created
        - 400 Bad Request: Invalid input data
        - 403 Forbidden: Missing required permissions
        - 500 Server Error: Unexpected error
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {"error": "You don't have permission to add categories"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create category: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EditCategoryView(UpdateAPIView):
    """API endpoint for updating existing categories.

    Permissions:
    - Requires 'edit_category' permission

    Methods:
    - PATCH: Partial update of category
    - PUT: Not allowed (returns 405)
    """

    permission_classes = [HasCoursePermission]
    required_permission = 'edit_category'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'

    @swagger_auto_schema(
        operation_description="Update an existing category (partial update)",
        request_body=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: "Bad Request - Invalid input data",
            403: "Forbidden - Missing required permissions",
            404: "Not Found - Category doesn't exist",
            500: "Internal Server Error"
        },
        tags=['Categories'],
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_PATH,
                description="Name of the category to update",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        """Handle partial updates to categories.

        Returns:
        --------
        Response
            HTTP response with updated category data or error message

        Possible Status Codes:
        - 200 OK: Successfully updated
        - 400 Bad Request: Invalid input data
        - 403 Forbidden: Missing required permissions
        - 404 Not Found: Category doesn't exist
        - 500 Server Error: Unexpected error
        """
        try:
            return super().patch(request, *args, **kwargs)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {"error": "You don't have permission to edit categories"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update category: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="PUT method not allowed for categories",
        responses={
            405: "Method Not Allowed"
        },
        tags=['Categories']
    )
    def put(self, request, *args, **kwargs):
        """Handle PUT requests (not allowed).

        Returns:
        --------
        Response
            HTTP 405 Method Not Allowed response
        """
        return Response(
            {"error": "PUT method not allowed. Use PATCH for partial updates"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class DeleteCategoryView(DestroyAPIView):
    """API endpoint for deleting categories.

    Permissions:
    - Requires 'delete_category' permission

    Methods:
    - DELETE: Remove a category
    """

    permission_classes = [HasCoursePermission]
    required_permission = 'delete_category'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'

    @swagger_auto_schema(
        operation_description="Delete a category",
        responses={
            200: "OK - Category deleted successfully",
            403: "Forbidden - Missing required permissions",
            404: "Not Found - Category doesn't exist",
            500: "Internal Server Error"
        },
        tags=['Categories'],
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_PATH,
                description="Name of the category to delete",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        """Handle category deletion.

        Returns:
        --------
        Response
            HTTP response with a success/error message

        Possible Status Codes:
        - 200 OK: Successfully deleted
        - 403 Forbidden: Missing required permissions
        - 404 Not Found: Category doesn't exist
        - 500 Server Error: Unexpected error
        """
        try:
            category = self.get_object()
            self.perform_destroy(category)
            return Response(
                {"message": "Category deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDenied as e:
            return Response(
                {"error": "You don't have permission to delete categories"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to delete category: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListCategoryView(ListAPIView):
    """API endpoint for listing all categories.

    Permissions:
    - Public access (no authentication required)

    Methods:
    - GET: Retrieve all categories
    """

    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(
        operation_description="List all categories",
        responses={
            200: CategorySerializer(many=True),
            500: "Internal Server Error"
        },
        tags=['Categories'],
        manual_parameters=[
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Field to order results by",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Handle category listing.

        Returns:
        --------
        Response
            HTTP response with category list or error message

        Possible Status Codes:
        - 200 OK: Successfully retrieved list
        - 500 Server Error: Unexpected error
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve categories: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ViewCategory(RetrieveAPIView):
    """API endpoint for viewing a single category.

    Permissions:
    - Public access (no authentication required)

    Methods:
    - GET: Retrieve a specific category by name
    """

    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'name'

    @swagger_auto_schema(
        operation_description="Retrieve a specific category by name",
        responses={
            200: CategorySerializer,
            404: "Not Found - Category doesn't exist",
            500: "Internal Server Error"
        },
        tags=['Categories'],
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_PATH,
                description="Name of the category to retrieve",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        """Handle category retrieval.

        Returns:
        --------
        Response
            HTTP response with category data or error message

        Possible Status Codes:
        - 200 OK: Successfully retrieved
        - 404 Not Found: Category doesn't exist
        - 500 Server Error: Unexpected error
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve category: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

