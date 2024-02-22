import re

from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from api_yamdb.settings import MAX_USERNAME_LENGTH, MAX_EMAIL_LENGTH
from .validators import not_equal_me_username_validator
from .models import MyUser


class SignUpSerializer(serializers.Serializer):
    """Serializer for user registration."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator(), not_equal_me_username_validator]
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

    def send_email(self, email, confirmation_code):
        """Method for sending email."""
        send_mail(
            subject='Confirmation code for Yamdb',
            message=f'Добрый день! Ваш код подтверждения: {confirmation_code}',
            from_email='mail@yamdb.com',
            recipient_list=[email],
            fail_silently=True
        )

    def create(self, validated_data):
        """
        Create and return a new `MyUser` instance, given the validated data,
        send confirmation code on email.
        """
        username = self.initial_data.get('username')
        email = self.initial_data.get('email')
        user, created = MyUser.objects.get_or_create(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        self.send_email(email, confirmation_code)
        return user


class CustomTokenObtainSerializer(serializers.Serializer):
    """Serializer to get a token."""

    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator, not_equal_me_username_validator]
    )
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


class UserEditSerializer(UserSerializer):
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
