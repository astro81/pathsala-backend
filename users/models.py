import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        STUDENT = 'student', 'Student'

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
        validators=[EmailValidator(message="Enter a valid email address.")],
        verbose_name="Email Address",
        help_text="User's unique email address."
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
        verbose_name="User Role",
        help_text="Primary role determining user permissions and access level."
    )

    class Meta:
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
            models.Index(fields=['date_joined']),
        ]

    def __str__(self):
        return self.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Address",
        help_text="Residential address of the user."
    )

    phone_no = models.CharField(
        max_length=15,
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

    is_approved = models.BooleanField(
        default=False,
        verbose_name="Is Approved",
        help_text="Indicates whether the student has been approved to enroll in the course."
    )

    def __str__(self):
        return self.user.username


