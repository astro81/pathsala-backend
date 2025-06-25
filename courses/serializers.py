from rest_framework import serializers

from course_description.models import CourseDescription
from course_description.serializers import CourseDescriptionSerializer
from course_syllabus.models import CourseSyllabus, CourseSyllabusTitleContent
from course_syllabus.serializers import CourseSyllabusSerializer
from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):

    description = CourseDescriptionSerializer(required=False, allow_null=True)
    syllabus = CourseSyllabusSerializer(required=False, allow_null=True)

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
        syllabus_data = validated_data.pop('syllabus', None)

        course = Course.objects.create(**validated_data)

        if description_data:
            course.description = CourseDescription.objects.create(**description_data)
            course.save()

        if syllabus_data:
            # Create syllabus and its contents
            syllabus_contents = syllabus_data.pop('course_syllabus_title_contents', [])
            syllabus = CourseSyllabus.objects.create(**syllabus_data)

            for content_data in syllabus_contents:
                CourseSyllabusTitleContent.objects.create(
                    syllabus_title_id=syllabus,
                    **content_data
                )

            course.syllabus = syllabus

        return course

    def _handle_description_update(self, instance, description_data):
        if description_data is None:
            instance.description = None
        elif instance.description:
            # Update existing description
            for field, value in description_data.items():
                setattr(instance.description, field, value)
            instance.description.save()
        else:
            # Create new description
            instance.description = CourseDescription.objects.create(**description_data)

    def _handle_syllabus_update(self, instance, syllabus_data):
        if syllabus_data is None:
            instance.syllabus = None
        elif instance.syllabus:
            # Update existing syllabus
            syllabus = instance.syllabus
            contents = syllabus_data.pop('course_syllabus_title_contents', None)

            for field, value in syllabus_data.items():
                setattr(syllabus, field, value)
            syllabus.save()

            # Update contents if provided
            if contents is not None:
                syllabus.course_syllabus_title_contents.all().delete()
                for content_data in contents:
                    CourseSyllabusTitleContent.objects.create(
                        syllabus_title_id=syllabus,
                        **content_data
                    )
        else:
            # Create new syllabus with contents
            contents = syllabus_data.pop('course_syllabus_title_contents', [])
            syllabus = CourseSyllabus.objects.create(**syllabus_data)

            for content_data in contents:
                CourseSyllabusTitleContent.objects.create(
                    syllabus_title_id=syllabus,
                    **content_data
                )

            instance.syllabus = syllabus

    def update(self, instance, validated_data):
        # Handle description update
        if 'description' in validated_data:
            self._handle_description_update(instance, validated_data.pop('description'))

        # Handle syllabus update
        if 'syllabus' in validated_data:
            self._handle_syllabus_update(instance, validated_data.pop('syllabus'))

        # Update basic course fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance