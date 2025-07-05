from rest_framework import serializers
from enrollment.models import Enrollment
from courses.serializers import CourseSerializer
from users.serializers import UserSerializer


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
        exclude = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        return Enrollment.objects.create(user=user, **validated_data)