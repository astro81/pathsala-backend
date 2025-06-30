"""Models for the course management system.

This module defines the Course model which represents educational courses in the system.
It includes fields for course details, metadata, and related utility methods.
"""

import uuid
from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from category.models import Category

User = get_user_model()


class Course(models.Model):
    """Represents an educational course in the system.

    This model stores all information related to a course, including its metadata,
    pricing, duration, and curriculum details.

    Attributes
    ----------
    TRAINING_LEVELS : list of tuple
        Available choices for course difficulty levels.
    CLASS_TYPES : list of tuple
        Available choices for course delivery methods.

    Fields
    ------
    id : UUIDField
        Primary key for the course (auto-generated).
    name : CharField
        Short identifier for the course (unique).
    title : CharField
        Full descriptive title of the course.
    duration_weeks : PositiveIntegerField
        Length of course in weeks (minimum 1).
    price : DecimalField
        Cost of the course (non-negative).
    training_level : CharField
        Difficulty level (beginner/intermediate/advanced).
    class_type : CharField
        Delivery method (online/offline/hybrid).
    image : ImageField
        Promotional image for the course.
    created_at : DateTimeField
        When the course was created (auto-set).
    updated_at : DateTimeField
        When the course was last updated (auto-set).
    overview : TextField
        Detailed description of the course.
    objectives : TextField
        Learning goals (one per line).
    prerequisites : TextField
        Required knowledge (one per line).
    outcomes : TextField
        Expected results (one per line).
    curriculum : JSONField
        Structured weekly content.
    owner : ForeignKey
        User who created the course.
    categories : ManyToManyField
        Categories this course belongs to.
    """

    TRAINING_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]

    CLASS_TYPES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid')
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the course"
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Short name of the course (e.g., Python Basics)"
    )

    title = models.CharField(
        max_length=500,
        help_text="Full title or description of the course"
    )

    duration_weeks = models.PositiveIntegerField(
        default=4,
        validators=[
            MinValueValidator(1, message=_("Duration must be at least 1 week")),
        ],
        help_text="Course duration in weeks"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00, message=_("Price cannot be negative"))],
        help_text="Course price in NPR"
    )

    training_level = models.CharField(
        max_length=100,
        choices=TRAINING_LEVELS,
        default='beginner',
        help_text="Skill level required to take this course"
    )

    class_type = models.CharField(
        max_length=100,
        choices=CLASS_TYPES,
        default='online',
        help_text="Type of class delivery"
    )

    image = models.ImageField(
        upload_to='courses/images/',
        null=True,
        blank=True,
        help_text="Course promotional image"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when course was created"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when course was last updated"
    )

    overview = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed course overview and introduction"
    )

    objectives = models.TextField(
        blank=True,
        help_text="Learning objectives (one per line)"
    )

    prerequisites = models.TextField(
        blank=True,
        help_text="Required knowledge before taking this course (one per line)"
    )

    outcomes = models.TextField(
        blank=True,
        help_text="What students will achieve (one per line)"
    )

    curriculum = models.JSONField(
        blank=True,
        default=list,
        help_text="Weekly curriculum structure"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        help_text="User who created this course"
    )

    categories = models.ManyToManyField(
        Category,
        related_name='category',
        help_text="Categories this course belongs to"
    )

    class Meta:
        """Metadata options for the Course model.

        Attributes
        ----------
        verbose_name : str
            Human-readable singular name.
        verbose_name_plural : str
            Human-readable plural name.
        ordering : list
            Default ordering for queries.
        indexes : list
            Database indexes for performance.
        """

        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['duration_weeks', 'price', '-created_at', 'training_level']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['duration_weeks']),
            models.Index(fields=['price']),
            models.Index(fields=['training_level']),
        ]

    def __str__(self):
        """String representation of the Course.

        Returns
        -------
        str
            Combination of course name and title.
        """
        return f"{self.name} - {self.title}"

    def save(self, *args, **kwargs):
        """Override save method to handle database errors gracefully.

        Raises
        ------
        ValidationError
            If database integrity or other errors occur during save.
        """
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValidationError({"error": f"Database integrity error: {str(e)}"})
        except DatabaseError as e:
            raise ValidationError({"error": f"Database error occurred: {str(e)}"})

    @property
    def duration_display(self):
        """Format duration for display purposes.

        Returns
        -------
        str
            Formatted duration string (e.g., "1 week" or "4 weeks").
        """
        try:
            if self.duration_weeks == 1:
                return "1 week"
            return f"{self.duration_weeks} weeks"
        except AttributeError:
            return {"error": "Duration not available"}

    @property
    def average_rating(self):
        """Calculate the average rating from all course ratings.

        Returns
        -------
        float
            Average rating (0.0 if no ratings or error occurs).
        """
        from django.db.models import Avg
        try:
            result = self.ratings.aggregate(average=Avg('rating'))
            return result['average'] if result['average'] is not None else 0.0
        except Exception as e:
            return 0.0

    def get_objectives_list(self):
        """Convert objectives text to a cleaned list.

        Returns
        -------
        list
            List of objectives (empty list if none or error).
        """
        try:
            return [obj.strip() for obj in self.objectives.split('\n') if obj.strip()]
        except AttributeError:
            return []

    def get_prerequisites_list(self):
        """Convert prerequisites text to a cleaned list.

        Returns
        -------
        list
            List of prerequisites (empty list if none or error).
        """
        try:
            return [preq.strip() for preq in self.prerequisites.split('\n') if preq.strip()]
        except AttributeError:
            return []

    def get_outcomes_list(self):
        """Convert outcomes text to a cleaned list.

        Returns
        -------
        list
            List of outcomes (empty list if none or error).
        """
        try:
            return [outcome.strip() for outcome in self.outcomes.split('\n') if outcome.strip()]
        except AttributeError:
            return []

