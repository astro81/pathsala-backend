import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="User ID",
        help_text="Unique identifier for the user."
    )

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Email Address",
        help_text="User's unique email address."
    )

    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Address",
        help_text="Residential address of the user."
    )

    phone_no = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?[0-9\-]{10,15}$')],
        verbose_name="Phone Number",
        help_text="Contact phone number. Include country code (e.g. +997-9812345678)."
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name="Profile Picture",
        help_text="Optional profile picture uploaded by the user."
    )

    def __str__(self):
        return self.username


