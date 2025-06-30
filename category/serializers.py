"""Serializers for the category system.

This module contains the serializer for converting between Category model instances
and JSON representations, including validation and data transformation logic.
"""

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model instances.

    Handles:
    - Serialization/deserialization of category data
    - Validation of category names
    - Automatic whitespace trimming of names

    Attributes
    ----------
    Meta : class
        Inner class containing metadata options
    """

    class Meta:
        """Metadata options for CategorySerializer.

        Attributes
        ----------
        model : Model
            The Category model class
        fields : str
            All model fields included in serialization
        """
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        """Validate and clean the category name.

        Parameters
        ----------
        value : str
            The raw category name to validate

        Returns
        -------
        str
            The cleaned and validated category name (stripped of whitespace)

        Raises
        ------
        ValidationError
            - If the name is empty after stripping whitespace
            - If the name contains only whitespace
            - For any unexpected validation errors

        Examples
        --------
        >>> serializer = CategorySerializer()
        >>> serializer.validate_name(" Programming ")  # Returns "Programming"
        >>> serializer.validate_name("   ")  # Raises ValidationError
        """
        try:
            stripped_value = value.strip()
            if not stripped_value:
                raise serializers.ValidationError(
                    {"error": "Category name cannot be empty or whitespace"},
                )
            return stripped_value
        except AttributeError as e:
            raise ValidationError(
                {"error": "Category name must be a string"},
            )
        except Exception as e:
            raise ValidationError(
                {"error": f"Invalid category name: {str(e)}"},
            )

