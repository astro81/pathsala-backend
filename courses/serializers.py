from rest_framework import serializers

from course_description.models import CourseDescription
from course_description.serializers import CourseDescriptionSerializer
from course_syllabus.models import CourseSyllabus
from course_syllabus.serializers import CourseSyllabusSerializer
from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):

    description = CourseDescriptionSerializer(required=False, allow_null=True)

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
        if 'duration' in data and isinstance(data['duration'], str):
            duration = data.pop('duration', None)
            try:
                value, unit = duration.split()
                data['duration'] = int(value)
                data['duration_unit'] = unit
                del data['duration_value']
            except ValueError:
                raise serializers.ValidationError({'duration': 'Invalid duration format. Expected "value unit".'})
        return super().to_internal_value(data)

    def create(self, validated_data):
        description_data = validated_data.pop('description', None)

        course = Course.objects.create(**validated_data)

        if description_data:
            course.description = CourseDescription.objects.create(**description_data)
            course.save()

        return course

    def update(self, instance, validated_data):
        description_data = validated_data.pop('description', None)

        # Update course fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update description if provided
        if description_data is not None:
            if instance.description:
                # Update existing description
                description_serializer = CourseDescriptionSerializer(
                    instance.description,
                    data=description_data,
                    partial=True
                )
                description_serializer.is_valid(raise_exception=True)
                description_serializer.save()
            elif description_data:
                # Create new description if data provided
                instance.description = CourseDescription.objects.create(**description_data)
            else:
                # description_data is None, which means we should set description to None
                instance.description = None

        instance.save()
        return instance

