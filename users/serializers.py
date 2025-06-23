import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This username is already taken.")
        ],
        min_length=4,
        max_length=30,
        help_text="Required. 4-30 characters. Letters, digits and @/./+/-/_ only."
    )

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This email is already registered.")
        ],
        style={'input_type': 'email'},
        help_text="A valid email address is required."
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        required=True,
        style={'input_type': 'password'},
        help_text="Required. 8-128 characters. Must include uppercase, lowercase, number and special character."
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        required=True,
        style={'input_type': 'password'},
        help_text = "Enter the same password as above, for verification."
    )

    phone_no = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=15,
        help_text="Optional. Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'address',
            'phone_no',
            'profile_picture',
            'last_login',
            'date_joined',
            'is_active'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        # Additional email validation if needed
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise serializers.ValidationError("Enter a valid email address.")

        return value.lower()  # Normalize email to lowercase

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        # Additional custom password validation
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    def validate_phone_no(self, value):
        if not value:  # Allow empty/null
            return value

        # Phone number validation
        if not re.match(r'^\+?[0-9\-]{10,15}$', value):
            raise serializers.ValidationError(
                "Phone number must be 10-15 digits, can start with + and contain hyphens."
            )

        # Remove any non-digit characters except leading +
        cleaned = re.sub(r'(?!^\+)[^0-9]', '', value)
        return cleaned

    def validate(self, data):

        if 'id' in data:
            data.pop('id')

        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'error': 'Passwords must match.'})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    def _validate_unique_field(self, instance, field_name, value):
        if value and User.objects.exclude(pk=self.instance.pk).filter(**{field_name: value}).exists():
            raise serializers.ValidationError({'error': f"This {field_name.replace('_', ' ')} is already taken."})

    def update(self, instance, validated_data):

        if 'id' in validated_data:
            validated_data.pop('id')

        validated_data.pop('password2', None)

        self._validate_unique_field(instance, 'username', validated_data.get('username'))
        self._validate_unique_field(instance, 'email', validated_data.get('email'))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password := validated_data.pop('password', None):
            instance.set_password(password)

        instance.save()
        return instance


