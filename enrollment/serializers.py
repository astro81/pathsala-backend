from django.utils import timezone

from rest_framework import serializers
from enrollment.models import Enrollment
from courses.serializers import CourseSerializer
from users.serializers import UserSerializer


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = '__all__'


    def create(self, validated_data):
        if validated_data.get('status') == 'approved':
            validated_data['Enrolled_Date'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('status') and instance.status != 'approved':
            validated_data['Enrolled_Date'] = timezone.now()
        return super().update(instance, validated_data)


