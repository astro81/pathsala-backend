from rest_framework import serializers
from enrollment.models import Enrollment
from courses.serializers import CourseSerializer
from courses.models import Course
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']


class CourseEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'title']


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.

    This serializer handles the conversion of Enrollment model instances to JSON
    and vice versa, including all fields from the model. It inherits from Django
    REST Framework's ModelSerializer which provides default implementations for
    create and update operations.

    The serializer includes nested representations of related User and Course objects
    through their respective serializers.

    Attributes
    ----------
    Meta : class
        Inner class containing metadata for the serializer.
    """

    user = StudentEnrollmentSerializer(read_only=True)

    course = CourseEnrollmentSerializer(read_only=True)  # show course details
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True,
        source='course'
    )


    class Meta:
        """
        Metadata options for the EnrollmentSerializer.

        Attributes
        ----------
        model : Model
            The Django model associated with this serializer (Enrollment).
        fields : str
            Specifies that all fields from the model should be included in the serialization.
            Uses '__all__' to automatically include all model fields.
        """

        model = Enrollment
        fields = '__all__'
        # exclude = ['user']

    def create(self, validated_data):
        user = self.context['request'].user.id  # Id of a user from provided access token of a user.
        return Enrollment.objects.create(user_id=user, **validated_data)


