from rest_framework import serializers

from course_description.models import CourseDescription
from course_description.serializers import CourseDescriptionSerializer
from course_syllabus.models import CourseSyllabus
from course_syllabus.serializers import CourseSyllabusSerializer
from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):

    description = CourseDescriptionSerializer()
    syllabus = CourseSyllabusSerializer()

    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'rating': {'min_value': 0, 'max_value': 5, 'required': False},
            'price': {'min_value': 0, 'required': False},
        }


    def get_duration(self, obj):
        return obj.duration_display

    def to_internal_value(self, data):
        if 'duration' in data:
            duration = data.pop('duration', None)
            try:
                value, unit = duration.split()
                data['duration'] = int(value)
                data['duration_unit'] = unit
            except ValueError:
                raise serializers.ValidationError({'duration': 'Invalid duration format. Expected "value unit".'})
        return super().to_internal_value(data)

    def create(self, validated_data):
        description_data = validated_data.pop('description')
        syllabus_data = validated_data.pop('syllabus')

        description = CourseDescription.objects.create(**description_data)
        syllabus = CourseSyllabus.objects.create(**syllabus_data)

        course = Course.objects.create(
            description=description,
            syllabus=syllabus,
            **validated_data
        )
        return course

    def update(self, instance, validated_data):
        description_data = validated_data.pop('description')
        syllabus_data = validated_data.pop('syllabus')

        # Update course fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update description if provided
        if description_data:
            description = instance.description
            for attr, value in description_data.items():
                setattr(description, attr, value)
            description.save()

        if syllabus_data:
            syllabus = instance.syllabus
            for attr, value in syllabus_data.items():
                setattr(syllabus, attr, value)
            syllabus.save()

        instance.save()
        return instance

