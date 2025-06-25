import uuid
from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from course_description.models import CourseDescription
from course_syllabus.models import CourseSyllabus

class Course(models.Model):
    DURATION_UNITS = [
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
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

    duration_value = models.PositiveIntegerField(
        default=4,
        validators=[
            MinValueValidator(1),          #! At least 1 day
            MaxValueValidator(365)         #! Max 1 year
        ]
    )

    duration_unit = models.CharField(
        max_length=10,
        choices=DURATION_UNITS,
        default='weeks'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Course price in NPR"
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        help_text="Average course rating from 0.0 to 5.0"
    )

    training_level = models.CharField(
        max_length=100,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner',
        help_text="Skill level required to take this course"
    )

    class_type = models.CharField(
        max_length=100,
        choices=[
            ('online', 'Online'),
            ('offline', 'Offline'),
            ('hybrid', 'Hybrid')
        ],
        default='online',
        help_text="Type of class delivery"
    )

    career_prospect = models.CharField(
        max_length=100,
        help_text="Main career outcomes this course prepares for"
    )

    image = models.ImageField(
        upload_to='courses/images/',
        null=True,
        blank=True,
        help_text="Course promotional image"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    description = models.OneToOneField(CourseDescription, on_delete=models.CASCADE)
    courseSyllabus = models.OneToOneField(CourseSyllabus, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['duration_value', '-rating', 'price', '-created_at', 'training_level']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=[ 'duration_value']),
            models.Index(fields=['duration_unit']),
            models.Index(fields=['rating']),
            models.Index(fields=['price']),
            models.Index(fields=['training_level']),
        ]

    def __str__(self):
        return self.name

    @property
    def duration_display(self):
        return f"{self.duration_value} {self.duration_unit}"

    # todo: link category, syllabus and description table
    # category_id = models.CharField(max_length=100)
    # description_id = models.TextField()
    # syllabus_id = models.TextField()


