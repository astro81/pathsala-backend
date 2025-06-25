import uuid
from django.db import models

# Create your models here.

class CourseSyllabus(models.Model):


    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(
        max_length=255,
        unique=True,
    )

    syllabus_title_indexing = models.PositiveIntegerField(
        null=False,
        blank=False,
        editable=True,  # in case of mistakes occur while making order of syllabus title
        unique=True,
    )

    class Meta:
        verbose_name = "CourseSyllabus"
        verbose_name_plural = "CourseSyllabus"
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['syllabus_title_indexing']),
        ]

    def __str__(self):
        return self.title


class CourseSyllabusTitleContent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )

    title_content = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    syllabus_title_content_indexing = models.PositiveIntegerField(
        null=False,
        blank=False,
        editable=True, # in case of mistakes occur while making order of syllabus title content
        unique=True,
    )

    syllabus_title_id = models.ForeignKey(
        CourseSyllabus,
        on_delete=models.CASCADE,

    )

    class Meta:
        verbose_name = "CourseSyllabusTitleContent"
        verbose_name_plural = "CourseSyllabusTitleContents"
        indexes = [
            models.Index(fields=['title_content']),
            models.Index(fields=['syllabus_title_content_indexing']),
        ]

    def __str__(self):
        return self.title_content

