import uuid

from django.db import models
from users.models import User
from courses.models import Course


# Create your models here.

class Enrollment(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    approved_by = models.CharField(
        choices = [
            ('admin', 'Admin'),
            ('moderator', 'Moderator'),
        ],
        null = True,
        blank = True,
    )

    status = models.CharField(
        choices = [('approved', 'Approved'),
            ('denied', 'Denied'),
            ('pending', 'Pending'),],
        default='pending',
    )

    Enrolled_Date = models.DateTimeField(
        null = True,
        blank = True,
        auto_now_add = True, #todo: will avoid in manual change of create or update both.
    )


    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )


