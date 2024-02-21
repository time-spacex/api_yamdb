import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers, status

from api_yamdb.settings import MAX_USERNAME_LENGTH, MAX_EMAIL_LENGTH
from .validators import NotEqualMeUsernameValidator
from .models import MyUser


class SignUpSerializer(serializers.Serializer):
    """Serializer for user registration."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator(), NotEqualMeUsernameValidator()]
    )
    email = serializers.EmailField(required=True, max_length=MAX_EMAIL_LENGTH)

    def validate(self, data):
        """
        Validation method for checking existing users' input into data fields.
        """
        user_with_email_exists = MyUser.objects.filter(email=data.get('email')).first()
        user_with_username_exists = MyUser.objects.filter(username=data.get('username')).first()
        if user_with_email_exists != user_with_username_exists:
            error_msg = {}
            if user_with_email_exists:
                error_msg['email'] = 'Пользователь с таким email уже существует'
            if user_with_username_exists:
                error_msg['username'] = 'Пользователь с таким username уже существует'
            raise serializers.ValidationError(error_msg, code=status.HTTP_400_BAD_REQUEST)
        return data

    def create(self, validated_data):
        """
        Create and return a new `MyUser` instance, given the validated data.
        """
        return MyUser.objects.create(**validated_data)


class CustomTokenObtainSerializer(serializers.Serializer):
    """Serializer to get a token."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for receiving and editing user data."""

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        if (
            len(value) >= 150
            or not re.match(r'^[\w.@+-]+\Z', value)
            or value.lower() == 'me'
        ):
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value


class UserEditSerializer(serializers.ModelSerializer):
    """Serializer for receiving and editing data about your profile."""

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        if value.lower() == 'me':
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value
