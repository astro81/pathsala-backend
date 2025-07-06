from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from course_ratings.models import CourseRating

@receiver(post_save, sender=CourseRating)
def update_course_on_rating_save(sender, instance, created, **kwargs):
    """Signal to update course rating when new rating is saved."""
    if created:  # Only update if this is a new rating
        instance.course.update_average_rating()

@receiver(post_delete, sender=CourseRating)
def update_course_on_rating_delete(sender, instance, **kwargs):
    """Signal to update course rating when a rating is deleted."""
    instance.course.update_average_rating()