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
    - Category management through list input (using 'categories' field for both read/write)
    - Rating information inclusion
    - Proper error handling for database operations
    - Backward compatibility with 'categories_input' during transition

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
        Read-only list of category names (default)
    categories : ListField
        Write-only field when creating/updating (context-sensitive)
    categories_input : ListField
        Write-only field maintained for backward compatibility
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

    # Primary field for categories (context-sensitive)
    categories = serializers.SerializerMethodField(
        read_only=True,
        help_text="List of category names associated with the course"
    )

    # Backward compatibility field
    categories_input = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="DEPRECATED: Use 'categories' instead. List of category names for course association"
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
            'image': {'read_only': True},
        }

    def get_fields(self):
        """Dynamically adjust fields based on request method.

        Adds a write-only version of the 'categories' field for create/update operations
        while maintaining a read-only version for list/retrieve operations.
        """
        fields = super().get_fields()

        # Add write-only categories field for write operations
        if self.context.get('request') and self.context['request'].method in ['POST', 'PUT', 'PATCH']:
            fields['categories'] = serializers.ListField(
                child=serializers.CharField(),
                write_only=True,
                required=False,
                help_text="List of category names for course association"
            )
        return fields

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

    def validate(self, data):
        """Handle backward compatibility for categories_input.

        If categories_input is provided but categories is not, copy the value
        to categories to maintain backward compatibility during transition.
        """
        if 'categories_input' in data and 'categories' not in data:
            data['categories'] = data['categories_input']
        return data

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
            # Extract categories if provided (using the new field name)
            category_names = validated_data.pop('categories', [])

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
            # Handle categories update if provided (using new field name)
            if 'categories' in validated_data:
                category_names = validated_data.pop('categories')
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


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for Course model with specific fields for listing operations.

    This serializer handles both serialization (read) and deserialization (write)
    operations for Course objects, with additional computed fields for ratings
    and categories. Uses consistent 'categories' field name for both read/write.

    Attributes
    ----------
    average_rating : DecimalField
        Computed field representing the average rating from all course ratings
    ratings_count : SerializerMethodField
        Computed field for total number of ratings
    categories : SerializerMethodField
        Computed field for list of associated category names (read)
    categories : ListField
        Write-only field when creating/updating (context-sensitive)
    categories_input : ListField
        Write-only field maintained for backward compatibility
    """

    avg_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        read_only=True,
        help_text="Average rating from all course ratings (range: 0.00-5.00)"
    )

    ratings_count = serializers.SerializerMethodField(
        read_only=True,
        help_text="Total number of ratings submitted for this course"
    )

    # Primary field for categories (context-sensitive)
    categories = serializers.SerializerMethodField(
        read_only=True,
        help_text="List of category names associated with the course"
    )

    # Backward compatibility field
    categories_input = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="DEPRECATED: Use 'categories' instead. List of category names to associate with course"
    )

    class Meta:
        """Metadata options for the CourseListSerializer.

        Attributes
        ----------
        model : Course
            The Django model class being serialized
        fields : list
            Complete list of fields to include in serialization,
            combining model fields and custom computed fields
        """
        model = Course
        fields = [
            'id',
            'name',
            'title',
            'overview',
            'duration_weeks',
            'price',
            'training_level',
            'class_type',
            'image',
            'avg_rating',
            'ratings_count',
            'categories',
            'categories_input',
            'created_at'
        ]

    def get_fields(self):
        """Dynamically adjust fields based on request method.

        Adds write-only version of 'categories' field for create/update operations
        while maintaining read-only version for list/retrieve operations.
        """
        fields = super().get_fields()

        # Add write-only categories field for write operations
        if self.context.get('request') and self.context['request'].method in ['POST', 'PUT', 'PATCH']:
            fields['categories'] = serializers.ListField(
                child=serializers.CharField(),
                write_only=True,
                required=False,
                help_text="List of category names for course association"
            )
        return fields

    def validate(self, data):
        """Handle backward compatibility for categories_input.

        If categories_input is provided but categories is not, copy the value
        to categories to maintain backward compatibility during transition.
        """
        if 'categories_input' in data and 'categories' not in data:
            data['categories'] = data['categories_input']
        return data

    def get_categories(self, obj):
        """Retrieve category names associated with the course.

        Parameters
        ----------
        obj : Course
            The course instance being serialized

        Returns
        -------
        list[str]
            Alphabetical list of category names, or empty list on error
        """
        try:
            return [category.name for category in obj.categories.all()]
        except Exception as e:
            return []

    def get_ratings_count(self, obj):
        """Count all ratings associated with the course.

        Parameters
        ----------
        obj : Course
            The course instance being serialized

        Returns
        -------
        int
            Total number of ratings for this course
        """
        return obj.ratings.count()


class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['image']
        extra_kwargs = {
            'image': {'required': True}
        }

