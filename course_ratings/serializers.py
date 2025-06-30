"""Serializers for the course rating system.

This module contains the serializer for converting between CourseRating model instances
and JSON representations, including validation and data transformation logic.
"""

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from course_ratings.models import CourseRating


class CourseRatingSerializer(serializers.ModelSerializer):
    """Serializer for CourseRating model instances.

    Handles:
    - Serialization/deserialization of rating data
    - Validation of rating values
    - Read-only representations of related objects
    - Protection of system-managed fields

    Attributes
    ----------
    user : StringRelatedField
        Read-only representation of the associated user (shows string representation)
    course : StringRelatedField
        Read-only representation of the associated course (shows string representation)
    """

    user = serializers.StringRelatedField(
        read_only=True,
        help_text="String representation of the user who created the rating"
    )
    course = serializers.StringRelatedField(
        read_only=True,
        help_text="String representation of the course being rated"
    )

    class Meta:
        """Metadata options for CourseRatingSerializer.

        Attributes
        ----------
        model : Model
            The CourseRating model class
        fields : list
            Fields to include in serialization (all relevant fields)
        read_only_fields : list
            Fields that should not be modified during updates (system-managed fields)
        """
        model = CourseRating
        fields = [
            'id',          # System-generated unique identifier
            'course',       # Associated course (read-only)
            'user',        # Associated user (read-only)
            'rating',      # Numeric rating value (0.0-5.0)
            'review',      # Optional text review
            'created_at',  # Creation timestamp
            'updated_at'   # Last update timestamp
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]

    def validate_rating(self, value):
        """Validate that the rating falls within the acceptable range (0.0-5.0).

        Parameters
        ----------
        value : decimal.Decimal
            The rating value to validate

        Returns
        -------
        decimal.Decimal
            The validated rating value

        Raises
        ------
        ValidationError
            If the rating is outside the valid range (0.0-5.0)
            If the rating value is invalid or malformed

        Examples
        --------
        >>> serializer = CourseRatingSerializer()
        >>> serializer.validate_rating(4.5)  # Valid
        4.5
        >>> serializer.validate_rating(6.0)  # Invalid
        ValidationError: {"error": "Rating must be between 0 and 5"}
        """
        try:
            if value < 0 or value > 5:
                raise serializers.ValidationError(
                    {"error": "Rating must be between 0 and 5"},
                    code='invalid_rating_range'
                )
            return value
        except Exception as e:
            raise ValidationError(
                {"error": f"Invalid rating value: {str(e)}"},
                code='invalid_rating_format'
            )

    def create(self, validated_data):
        """Create a new CourseRating instance with additional validation.

        Parameters
        ----------
        validated_data : dict
            Validated data for rating creation

        Returns
        -------
        CourseRating
            The newly created rating instance

        Raises
        ------
        ValidationError
            If the user has already rated this course
            If any other error occurs during creation
        """
        try:
            # Get current user from request context
            user = self.context['request'].user
            course = validated_data.get('course')

            # Prevent duplicate ratings
            if CourseRating.objects.filter(user=user, course=course).exists():
                raise ValidationError(
                    {"error": "You have already rated this course"},
                    code='duplicate_rating'
                )

            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(
                {"error": f"Failed to create rating: {str(e)}"},
                code='creation_failed'
            )

