import uuid
from django.db import models
from users.models import User
from courses.models import Course


class Enrollment(models.Model):
    """
    Represents a user's enrollment request for a course in the system.

    This model tracks the enrollment process including approval status, dates,
    and the responsible parties for approval.

    Attributes
    ----------
    id : UUIDField
        A unique identifier for the enrollment record (primary key).
    approved_by : CharField
        The role that approved the enrollment (admin/moderator). Can be null if not approved yet.
    status : CharField
        Current status of the enrollment (approved/denied/pending).
    applied_Date : DateTimeField
        The date when the enrollment was initially requested (auto-set on creation).
    Enrolled_Date : DateTimeField
        The date when the enrollment was approved and processed. Can be null if not approved.
    course : ForeignKey
        Reference to the Course being enrolled in.
    user : ForeignKey
        Reference to the User who is enrolling.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the enrollment record"
    )

    approved_by = models.CharField(
        choices=[
            ('admin', 'Admin'),
            ('moderator', 'Moderator'),
        ],
        null=True,
        blank=True,
        help_text="Role of the person who approved this enrollment"
    )

    status = models.CharField(
        choices=[
            ('approved', 'Approved'),
            ('denied', 'Denied'),
            ('pending', 'Pending'),
        ],
        default='pending',
        help_text="Current status of the enrollment request"
    )

    applied_Date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date when the enrollment was first applied for"
    )

    Enrolled_Date = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=False,
        help_text="Date when the enrollment was officially processed"
    )

    whatsApp = models.CharField(
        null=False,
        blank=False,
        help_text="WhatsApp app number of a enroll person",
    )

    refer_by = models.CharField(
        null=True,
        blank=True,
        help_text="WhatsApp app number of a person who refer to the enrollment",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        help_text="The course being enrolled in"
    )

    fullName = models.CharField(
        null=False,
        blank=False,
    )

    email = models.EmailField(
        null=False,
        blank=False,
    )


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        help_text="The user requesting enrollment"
    )

    class Meta:
        """Metadata options for the Enrollment model."""
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        ordering = ['-applied_Date']

    def __str__(self):
        """
        Return a human-readable string representation of the enrollment.

        Returns
        -------
        str
            String in format: "[user] enrollment for [course] - [status]"
        """
        return f"{self.user} enrollment for {self.course} - {self.status}"