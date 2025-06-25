import uuid

from django.db import models

# Create your models here.
class CourseDescription(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    course_introduction = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Course introduction"
    )

    course_overview = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Course overview"
    )

    course_requirements = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Course requirements"
    )

    course_context = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Course context"
    )

