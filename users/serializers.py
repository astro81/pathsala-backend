from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rolepermissions.roles import assign_role

from users.models import Student, Moderator
from users.validators import validate_email_format, validate_strong_password, validate_phone_number

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role'
        ]


class UserCreateUpdateMixin:
    """Mixin for common user registration/update functionality"""

    def validate_username(self, value):
        """Validate username uniqueness"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        """Validate email format and uniqueness"""
        validate_email_format(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        """Validate password strength"""
        validate_strong_password(value)
        return value

    def validate(self, data):
        """Common validation for password confirmation and cleanup"""
        # Remove id if accidentally included
        if 'id' in data:
            data.pop('id')

        # Check password confirmation
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"error": "Passwords do not match"})

        return data

    def create_user(self, validated_data, role):
        """Create user with specified role"""
        return User.objects.create(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=make_password(validated_data.pop('password')),
            first_name=validated_data.pop('first_name', ''),
            last_name=validated_data.pop('last_name', ''),
            role=role
        )

    def update_user_fields(self, user, validated_data):
        """Update user fields and return if password was changed"""
        password_changed = False

        # Extract user-related fields
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)  # Discard confirmation

        # Update user fields if provided
        if username:
            if User.objects.exclude(pk=user.pk).filter(username=username).exists():
                raise serializers.ValidationError({"username": "Username already exists"})
            user.username = username

        if email:
            validate_email_format(email)
            if User.objects.exclude(pk=user.pk).filter(email=email).exists():
                raise serializers.ValidationError({"email": "Email already exists"})
            user.email = email

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if password:
            validate_strong_password(password)
            user.set_password(password)
            password_changed = True

        user.save()
        return password_changed

    def invalidate_user_tokens(self, user):
        """Invalidate all outstanding tokens for the user"""
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)


class ModeratorSerializer(UserCreateUpdateMixin, serializers.ModelSerializer):
    # Define user-related fields directly in the class
    id = serializers.UUIDField(source='user.id', read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Moderator
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
        ]

    def create(self, validated_data):
        validated_data.pop('password2')
        try:
            with transaction.atomic():
                user = self.create_user(validated_data, User.Role.MODERATOR)
                moderator = Moderator.objects.create(user=user, **validated_data)
                assign_role(user, 'moderator')
                return moderator
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def update(self, instance, validated_data):
        password_changed = self.update_user_fields(instance.user, validated_data)

        # Update moderator fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if password_changed:
            self.invalidate_user_tokens(instance.user)

        return instance


class StudentSerializer(UserCreateUpdateMixin, serializers.ModelSerializer):
    # Define user-related fields directly in the class
    id = serializers.UUIDField(source='user.id', read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'address',
            'phone_no',
            'profile_picture'
        ]
        extra_kwargs = {
            'profile_picture': {'required': False},
        }

    def validate_phone_no(self, value):
        """Validate phone number format"""
        if value:
            validate_phone_number(value)
            return value
        return None

    def create(self, validated_data):
        try:
            with transaction.atomic():
                validated_data.pop('password2')
                user = self.create_user(validated_data, User.Role.STUDENT)
                student = Student.objects.create(user=user, **validated_data)
                assign_role(user, 'student')
                return student
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def update(self, instance, validated_data):
        password_changed = self.update_user_fields(instance.user, validated_data)

        # Update student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if password_changed:
            self.invalidate_user_tokens(instance.user)

        return instance