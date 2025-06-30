"""Models for the category system.

This module defines the Category model which represents course categories
in the system, with name uniqueness enforcement and proper error handling.
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError


class Category(models.Model):
    """Represents a category for organizing courses.

    Attributes
    ----------
    id : UUIDField
        Primary key (auto-generated UUID)
    name : CharField
        Unique name of the category (required)

    Methods
    -------
    save(*args, **kwargs)
        Overrides save with comprehensive error handling
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the category (auto-generated)"
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        help_text="Name of the category (must be unique and is required)"
    )

    class Meta:
        """Metadata options for Category model.

        Attributes
        ----------
        verbose_name : str
            Singular name for admin interface
        verbose_name_plural : str
            Plural name for admin interface
        indexes : list
            Database indexes for performance
        ordering : list
            Default queryset ordering
        """
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [models.Index(fields=['name'])]
        ordering = ['name']

    def __str__(self):
        """String representation of the category.

        Returns
        -------
        str
            The category name
        """
        return self.name

    def save(self, *args, **kwargs):
        """Save the category with comprehensive error handling.

        Raises
        ------
        ValidationError
            - If a category name already exists (IntegrityError)
            - If a database error occurs (DatabaseError)
            - For any other unexpected error
        """
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValidationError(
                {"error": f"Category with this name already exists: {str(e)}"},
                code='unique_violation'
            )
        except DatabaseError as e:
            raise ValidationError(
                {"error": f"Database error occurred: {str(e)}"},
                code='database_error'
            )
        except Exception as e:
            raise ValidationError(
                {"error": f"Error saving category: {str(e)}"},
                code='unexpected_error'
            )

