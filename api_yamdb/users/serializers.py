import re
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from django.db.models import Q

from .models import MyUser


class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if len(value) >= 254:
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def validate_username(self, value):
        if len(value) >= 150 or not re.match(r'^[\w.@+-]+\Z', value) or value.lower() == "me":
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def validate(self, data):
        users = MyUser.objects.all()
        username = data.get('username')
        email = data.get('email')
        try:
            users.get(username=username, email=email)
            return data
        except MyUser.DoesNotExist:
            if users.filter(username=username).exists() or users.filter(email=email).exists():
                raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
            return data
        

    class Meta:
        model = MyUser
        fields = ('username', 'email')


class CustomTokenObtainSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)
