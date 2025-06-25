from rest_framework import serializers
from course_syllabus.models import CourseSyllabus, CourseSyllabusTitleContent


class CourseSyllabusContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSyllabusTitleContent
        fields = '__all__'


class CourseSyllabusSerializer(serializers.ModelSerializer):
    course_syllabus_title_contents = CourseSyllabusContentSerializer(many=True, required=False)

    class Meta:
        model = CourseSyllabus
        fields = '__all__'



