from rest_framework import serializers
from course_syllabus.models import CourseSyllabus, CourseSyllabusTitleContent

class CourseSyllabusSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSyllabus
        fields = '__all__'


class CourseSyllabusContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSyllabusTitleContent
        fields = '__all__'


