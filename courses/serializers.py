from rest_framework import serializers

from course_description.models import CourseDescription
from course_description.serializers import CourseDescriptionSerializer
from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):

    description = CourseDescriptionSerializer()

    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'rating': {'min_value': 0, 'max_value': 5, 'required': False},
            'price': {'min_value': 0, 'required': False},
        }

    def create(self, validated_data):
        description_data = validated_data.pop('description')
        description = CourseDescription.objects.create(**description_data)
        course = Course.objects.create(description=description, **validated_data)
        return course

    def update(self, instance, validated_data):
        description_data = validated_data.pop('description')

        # Update course fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update description if provided
        if description_data:
            description = instance.description
            for attr, value in description_data.items():
                setattr(description, attr, value)
            description.save()

        instance.save()
        return instance