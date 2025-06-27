import uuid

from django.db import models

# Create your models here.

class Category(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )


    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
