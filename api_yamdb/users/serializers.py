import re
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from .models import MyUser


class UserSerializer(serializers.ModelSerializer):

    confirmation_code = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ]
    )

    def validate_email(self, value):
        if len(value) >= 254:
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def validate_username(self, value):
        if len(value) >= 150 or not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        return value


    class Meta:
        model = MyUser
        fields = ['username', 'email', 'bio', 'role', 'first_name', 'last_name', 'confirmation_code']


class CustomTokenObtainSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    confirmation_code = serializers.CharField()