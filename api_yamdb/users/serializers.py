import re
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from .models import MyUser


class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ],
        required=True
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ],
        required=True
    )

    def validate_email(self, value):
        if len(value) >= 254:
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def validate_username(self, value):
        if len(value) >= 150 or not re.match(r'^[\w.@+-]+\Z', value) or value.lower() == "me":
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value

    class Meta:
        model = MyUser
        fields = ('username', 'email')


class CustomTokenObtainSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ],
        required=True
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ],
        required=True
    )

    def validate_email(self, value):
        if len(value) >= 254:
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def validate_username(self, value):
        if len(value) >= 150 or not re.match(r'^[\w.@+-]+\Z', value) or value.lower() == "me":
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value
    
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)
