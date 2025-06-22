from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This username is already taken.")
        ]
    )

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This email is already registered.")
        ]
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        style={'input_type': 'password'}
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
            'email': {'required': True, 'allow_blank': False, 'style': {'input_type': 'email'}},
        }

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'error': 'Passwords must match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Check unique username
        username = validated_data.get('username')
        if username and User.objects.exclude(pk=instance.pk).filter(username=username).exists():
            raise serializers.ValidationError({'error': 'This username is already taken.'})

        # Check unique email
        email = validated_data.get('email')
        if email and User.objects.exclude(pk=instance.pk).filter(email=email).exists():
            raise serializers.ValidationError({'error': 'This email is already registered.'})

        validated_data.pop('password2', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


