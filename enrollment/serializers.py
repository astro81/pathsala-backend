from django.utils import timezone

from rest_framework import serializers
from enrollment.models import Enrollment
from courses.serializers import CourseSerializer
from users.serializers import UserSerializer


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = '__all__'



