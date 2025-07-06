import django_filters
from django.db.models import Avg
from .models import Course


class CourseFilter(django_filters.FilterSet):
    """Filter for courses with support for rating ranges."""

    average_rating = django_filters.NumberFilter(
        method='filter_by_rating',
        help_text="Filter by exact average rating"
    )
    average_rating__gte = django_filters.NumberFilter(
        method='filter_by_rating_gte',
        help_text="Filter by minimum average rating"
    )
    average_rating__lte = django_filters.NumberFilter(
        method='filter_by_rating_lte',
        help_text="Filter by maximum average rating"
    )

    class Meta:
        model = Course
        fields = {
            'name': ['exact', 'icontains'],
            'title': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'duration_weeks': ['exact', 'gte', 'lte'],
            'training_level': ['exact'],
            'class_type': ['exact'],
            'categories__name': ['exact', 'icontains'],
        }

    def filter_by_rating(self, queryset, name, value):
        return queryset.filter(average_rating=value)

    def filter_by_rating_gte(self, queryset, name, value):
        return queryset.filter(average_rating__gte=value)

    def filter_by_rating_lte(self, queryset, name, value):
        return queryset.filter(average_rating__lte=value)