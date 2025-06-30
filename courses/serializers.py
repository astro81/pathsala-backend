"""Serializer for a Course model with extended functionality.

This serializer handles conversion between Course model instances and JSON data,
including special processing for objectives, prerequisites, outcomes, and categories.
"""

from django.db import IntegrityError, DatabaseError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from category.models import Category
from course_ratings.serializers import CourseRatingSerializer
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for the Course model with custom field processing.

    This serializer provides:
    - List-based input/output for text fields (objectives, prerequisites, outcomes)
    - Category management through list input
    - Rating information inclusion
    - Proper error handling for database operations

    Attributes
    ----------
    objectives : ListField
        Write-only field for objectives as list
    prerequisites : ListField
        Write-only field for prerequisites as list
    outcomes : ListField
        Write-only field for outcomes as list
    objectives_list : ListField
        Read-only representation of objectives as list
    prerequisites_list : ListField
        Read-only representation of prerequisites as list
    outcomes_list : ListField
        Read-only representation of outcomes as list
    average_rating : DecimalField
        Read-only average of all ratings
    ratings : CourseRatingSerializer
        Nested serializer for course ratings
    categories : SerializerMethodField
        Read-only list of category names
    categories_input : ListField
        Write-only field for category management
    """

    objectives = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of learning objectives (converted to newline-separated text)"
    )
    prerequisites = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of prerequisites (converted to newline-separated text)"
    )
    outcomes = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of learning outcomes (converted to newline-separated text)"
    )
    objectives_list = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        source='get_objectives_list',
        help_text="List representation of objectives"
    )
    prerequisites_list = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        source='get_prerequisites_list',
        help_text="List representation of prerequisites"
    )
    outcomes_list = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        source='get_outcomes_list',
        help_text="List representation of outcomes"
    )

    average_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        read_only=True,
        help_text="Average rating from all course ratings"
    )
    ratings = CourseRatingSerializer(
        many=True,
        read_only=True,
        help_text="Detailed rating information"
    )

    categories = serializers.SerializerMethodField(
        read_only=True,
        help_text="List of category names associated with the course"
    )

    categories_input = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of category names for course association"
    )

    class Meta:
        """Metadata options for CourseSerializer.

        Attributes
        ----------
        model : Model
            The Course model class
        fields : str
            All model fields included
        extra_kwargs : dict
            Additional field options
        """
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'categories': {'read_only': True}
        }

    def get_categories(self, obj):
        """Retrieve category names for serialization.

        Parameters
        ----------
        obj : Course
            The course instance being serialized

        Returns
        -------
        list
            List of category names or empty list on error
        """
        try:
            return [category.name for category in obj.categories.all()]
        except Exception:
            return []

    def create(self, validated_data):
        """Create a new Course instance with related data.

        Parameters
        ----------
        validated_data : dict
            Validated data for course creation

        Returns
        -------
        Course
            The created course instance

        Raises
        ------
        ValidationError
            If any error occurs during creation
        """
        try:
            # Extract categories if provided
            category_names = validated_data.pop('categories_input', [])

            # Convert lists to text fields
            if 'objectives' in validated_data:
                validated_data['objectives'] = '\n'.join(validated_data.pop('objectives'))
            if 'prerequisites' in validated_data:
                validated_data['prerequisites'] = '\n'.join(validated_data.pop('prerequisites'))
            if 'outcomes' in validated_data:
                validated_data['outcomes'] = '\n'.join(validated_data.pop('outcomes'))

            course = Course.objects.create(**validated_data)

            # Add categories
            for name in category_names:
                try:
                    category, _ = Category.objects.get_or_create(name=name.strip())
                    course.categories.add(category)
                except (IntegrityError, DatabaseError) as e:
                    raise ValidationError({"error": f"Error creating category '{name}': {str(e)}"})

            return course
        except Exception as e:
            raise ValidationError({"error": f"Error creating course: {str(e)}"})

    def update(self, instance, validated_data):
        """Update an existing Course instance with related data.

        Parameters
        ----------
        instance : Course
            The course instance to update
        validated_data : dict
            Validated data for course update

        Returns
        -------
        Course
            The updated course instance

        Raises
        ------
        ValidationError
            If any error occurs during the update
        """
        try:
            # Handle categories update if provided
            if 'categories_input' in validated_data:
                category_names = validated_data.pop('categories_input')
                instance.categories.clear()
                for name in category_names:
                    try:
                        category, _ = Category.objects.get_or_create(name=name.strip())
                        instance.categories.add(category)
                    except (IntegrityError, DatabaseError) as e:
                        raise ValidationError({"error": f"Error updating category '{name}': {str(e)}"})

            # Convert lists to text fields
            if 'objectives' in validated_data:
                validated_data['objectives'] = '\n'.join(validated_data['objectives'])
            if 'prerequisites' in validated_data:
                validated_data['prerequisites'] = '\n'.join(validated_data['prerequisites'])
            if 'outcomes' in validated_data:
                validated_data['outcomes'] = '\n'.join(validated_data['outcomes'])

            # Update other fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance
        except Exception as e:
            raise ValidationError({"error": f"Error updating course: {str(e)}"})

