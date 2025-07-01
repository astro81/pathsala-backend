"""Models for the course rating system.

This module defines the CourseRating model which handles:
- User ratings (0.0-5.0 scale) for courses
- Optional text reviews
- Automatic calculation of course average ratings
- Enforcement of one rating per user per course
"""

from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from decimal import Decimal
from courses.models import Course

User = get_user_model()


class CourseRating(models.Model):
    """Represents a user's rating and review for a course.

    Attributes
    ----------
    course : ForeignKey
        Reference to the Course being rated, with CASCADE deletion
    user : ForeignKey
        Reference to the User who created the rating, with CASCADE deletion
    rating : DecimalField
        Numeric rating (0.0-5.0) with precision of 3 digits (2 decimal places)
    review : TextField
        Optional detailed text review (can be blank or null)
    created_at : DateTimeField
        Automatic timestamp when rating was created
    updated_at : DateTimeField
        Automatic timestamp when rating was last updated

    Methods
    -------
    save(*args, **kwargs)
        Extends save with error handling and rating updates
    update_course_rating()
        Recalculates and updates the course's average rating
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='ratings',
        help_text="The course being rated (required)"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_ratings',
        help_text="User who submitted the rating (required)"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(Decimal("0.00"), message="Rating cannot be less than 0"),
            MaxValueValidator(Decimal("5.00"), message="Rating cannot exceed 5")
        ],
        help_text="Numeric rating between 0.0 and 5.0 (required)"
    )
    review = models.TextField(
        blank=True,
        null=True,
        help_text="Optional detailed review text (max 2000 chars)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Automatic timestamp when rating was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Automatic timestamp when rating was last updated"
    )

    class Meta:
        """Metadata options for the CourseRating model.

        Attributes
        ----------
        unique_together : list
            Ensures one rating per user per course combination
        ordering : list
            Default ordering by creation date (newest first)
        verbose_name : str
            Singular name for admin interface
        verbose_name_plural : str
            Plural name for admin interface
        """
        unique_together = ['course', 'user']
        ordering = ['-created_at']
        verbose_name = "Course Rating"
        verbose_name_plural = "Course Ratings"

    def save(self, *args, **kwargs):
        """Override save method with comprehensive error handling.

        Raises
        ------
        ValidationError
            If any database error occurs during save
            If rating update fails
        """
        try:
            super().save(*args, **kwargs)
            self.update_course_rating()
        except IntegrityError as e:
            raise ValidationError(
                {"error": f"Database integrity error: {str(e)}"},
            )
        except DatabaseError as e:
            raise ValidationError(
                {"error": f"Database error occurred: {str(e)}"},
            )
        except Exception as e:
            raise ValidationError(
                {"error": f"Unexpected error saving rating: {str(e)}"},
            )

    def update_course_rating(self):
        """Recalculate and update the course's average rating.

        Calculates a new average from all ratings and updates the course's
        rating field. Handles cases where no ratings exist.

        Raises
        ------
        ValidationError
            If the rating update process fails
        """
        try:
            from django.db.models import Avg
            ratings = self.course.ratings.all()
            average = ratings.aggregate(Avg('rating'))['rating__avg']
            self.course.rating = average or 0.0
            self.course.save()
        except Exception as e:
            raise ValidationError(
                {"error": f"Failed to update course rating: {str(e)}"},
            )

    def __str__(self):
        """String representation of the rating.

        Returns
        -------
        str
            Human-readable format: "CourseName - user@email.com: X.XX/5.0"
        """
        return f"{self.course.name} - {self.user.email}: {self.rating}/5.0"