from rest_framework import serializers

from course_description.models import CourseDescription


class CourseDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDescription
        fields = '__all__'
        extra_kwargs = {
            'course_introduction': {'required': False, 'allow_blank': True},
            'course_overview': {'required': False, 'allow_blank': True},
            'course_requirements': {'required': False, 'allow_blank': True},
            'course_context': {'required': False, 'allow_blank': True},
        }

