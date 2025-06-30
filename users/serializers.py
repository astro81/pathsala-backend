"""
User Management Serializers

This module provides Django REST Framework serializers for user registration and profile management,
with specific implementations for different user roles (Moderator, Student).

Classes:
    UserSerializer: Basic user profile serializer (read-only)
    UserCreateUpdateMixin: Shared functionality for user creation/update
    ModeratorSerializer: Handles moderator registration and updates
    StudentSerializer: Handles student registration and updates with additional profile fields
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rolepermissions.roles import assign_role

from users.models import Student, Moderator
from users.validators import (
    validate_email_format,
    validate_strong_password,
    validate_phone_number,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user profile serializer (read-only operations).

    Provides read-only access to core user fields without exposing sensitive information
    or allowing modifications.

    Fields:
        id: UUID (read-only)
        username: User's unique identifier
        email: User's email address
        first_name: User's first name
        last_name: User's last name
        role: User's role in the system
    """

    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        ]
        read_only_fields = fields  # All fields are read-only


class UserCreateUpdateMixin:
    """Mixin providing shared functionality for user creation and updates.

    Implements common validation and processing logic used by both Moderator
    and Student serializers.

    Methods:
        validate_username: Ensures username uniqueness
        validate_email: Validates email format and uniqueness
        validate_password: Enforces strong password requirements
        validate: Handles common validation logic
        create_user: Creates user with specified role
        update_user_fields: Updates user fields with validation
        invalidate_user_tokens: Blacklists all user's JWT tokens
    """

    def validate_username(self, value: str) -> str:
        """Validate username uniqueness.

        Parameters
        ----------
        value : str
            Proposed username

        Returns
        -------
        str
            Validated username

        Raises
        ------
        serializers.ValidationError
            If username already exists
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value: str) -> str:
        """Validate email format and uniqueness.

        Parameters
        ----------
        value : str
            Proposed email address

        Returns
        -------
        str
            Validated email address

        Raises
        ------
        serializers.ValidationError
            If email is invalid or already exists
        """
        validate_email_format(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value: str) -> str:
        """Validate password meets security requirements.

        Parameters
        ----------
        value : str
            Proposed password

        Returns
        -------
        str
            Validated password

        Raises
        ------
        serializers.ValidationError
            If password doesn't meet strength requirements
        """
        validate_strong_password(value)
        return value

    def validate(self, data: dict) -> dict:
        """Perform cross-field validation.

        Parameters
        ----------
        data : dict
            Input data dictionary

        Returns
        -------
        dict
            Validated data

        Raises
        ------
        serializers.ValidationError
            If passwords don't match or invalid fields present
        """
        # Remove id if accidentally included
        if "id" in data:
            data.pop("id")

        # Check password confirmation
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError({"error": "Passwords do not match"})

        return data

    def create_user(self, validated_data: dict, role: User.Role) -> User:
        """Create a new user with a specified role.

        Parameters
        ----------
        validated_data : dict
            Validated user data
        role : User.Role
            Role to assign to new user

        Returns
        -------
        User
            The created user instance
        """
        return User.objects.create(
            username=validated_data.pop("username"),
            email=validated_data.pop("email"),
            password=make_password(validated_data.pop("password")),
            first_name=validated_data.pop("first_name", ""),
            last_name=validated_data.pop("last_name", ""),
            role=role,
        )

    def update_user_fields(self, user: User, validated_data: dict) -> bool:
        """Update user fields with proper validation.

        Parameters
        ----------
        user : User
            User instance to update
        validated_data : dict
            Fields to update

        Returns
        -------
        bool
            True if the password was changed, False otherwise

        Raises
        ------
        serializers.ValidationError
            If username/email already exist or password is invalid
        """
        password_changed = False

        # Extract user-related fields
        username = validated_data.pop("username", None)
        email = validated_data.pop("email", None)
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)  # Discard confirmation

        # Update user fields if provided
        if username:
            if User.objects.exclude(pk=user.pk).filter(username=username).exists():
                raise serializers.ValidationError(
                    {"username": "Username already exists"}
                )
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

    def invalidate_user_tokens(self, user: User) -> None:
        """Invalidate all outstanding JWT tokens for a user.

        Parameters
        ----------
        user : User
            User whose tokens should be invalidated

        Notes
        -----
        This will immediately log out the user from all devices
        """
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)


class ModeratorSerializer(UserCreateUpdateMixin, serializers.ModelSerializer):
    """Serializer for moderator registration and profile updates.

    Handles creation and updates of moderator accounts with:
    - User account creation/update
    - Role assignment
    - Proper password handling
    - Token invalidation on password changes

    Fields:
        id: UUID (read-only, from user)
        username: Required unique identifier
        email: Required email address
        password: Required password (write-only)
        password2: Required password confirmation (write-only)
        first_name: Optional first name (write-only)
        last_name: Optional last name (write-only)
    """

    id = serializers.UUIDField(source="user.id", read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Moderator
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data: dict) -> Moderator:
        """Create a new moderator account.

        Parameters
        ----------
        validated_data : dict
            Validated input data

        Returns
        -------
        Moderator
            The created moderator instance

        Raises
        ------
        serializers.ValidationError
            If creation fails
        """
        validated_data.pop("password2")
        try:
            with transaction.atomic():
                user = self.create_user(validated_data, User.Role.MODERATOR)
                moderator = Moderator.objects.create(user=user, **validated_data)
                assign_role(user, "moderator")
                return moderator
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def update(self, instance: Moderator, validated_data: dict) -> Moderator:
        """Update an existing moderator account.

        Parameters
        ----------
        instance : Moderator
            Existing moderator instance to update
        validated_data : dict
            Fields to update

        Returns
        -------
        Moderator
            Updated moderator instance
        """
        password_changed = self.update_user_fields(instance.user, validated_data)

        # Update moderator fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if password_changed:
            self.invalidate_user_tokens(instance.user)

        return instance


class StudentSerializer(UserCreateUpdateMixin, serializers.ModelSerializer):
    """Serializer for student registration and profile updates.

    Handles creation and updates of student accounts with:
    - User account creation/update
    - Role assignment
    - Additional profile fields (address, phone, profile picture)
    - Proper password handling
    - Token invalidation on password changes

    Fields:
        id: UUID (read-only, from user)
        username: Required unique identifier
        email: Required email address
        password: Required password (write-only)
        password2: Required password confirmation (write-only)
        first_name: Optional first name (write-only)
        last_name: Optional last name (write-only)
        address: Optional address
        phone_no: Optional validated phone number
        profile_picture: Optional profile image
    """

    id = serializers.UUIDField(source="user.id", read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "address",
            "phone_no",
            "profile_picture",
        ]
        extra_kwargs = {
            "profile_picture": {"required": False},
        }

    def validate_phone_no(self, value: str) -> str:
        """Validate and format phone number.

        Parameters
        ----------
        value : str
            Input phone number

        Returns
        -------
        str
            Validated and formatted phone number

        Raises
        ------
        serializers.ValidationError
            If the phone number format is invalid
        """
        if value:
            validate_phone_number(value)
            return value
        return None

    def create(self, validated_data: dict) -> Student:
        """Create a new student account.

        Parameters
        ----------
        validated_data : dict
            Validated input data

        Returns
        -------
        Student
            The created student instance

        Raises
        ------
        serializers.ValidationError
            If creation fails
        """
        try:
            with transaction.atomic():
                validated_data.pop("password2")
                user = self.create_user(validated_data, User.Role.STUDENT)
                student = Student.objects.create(user=user, **validated_data)
                assign_role(user, "student")
                return student
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def update(self, instance: Student, validated_data: dict) -> Student:
        """Update an existing student account.

        Parameters
        ----------
        instance : Student
            Existing student instance to update
        validated_data : dict
            Fields to update

        Returns
        -------
        Student
            Updated student instance
        """
        password_changed = self.update_user_fields(instance.user, validated_data)

        # Update student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if password_changed:
            self.invalidate_user_tokens(instance.user)

        return instance

