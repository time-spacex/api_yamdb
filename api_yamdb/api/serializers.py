from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import serializers
from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'confirmation_code']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        confirmation_code = validated_data.get('confirmation_code', None)
        if not confirmation_code:
            confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            subject='Confirmation code for Yamdb',          
            message=f'Добрый день! Ваш код подтверждения: {confirmation_code}',  
            from_email='mail@yamdb.com',
            recipient_list=[validated_data['email']],
            fail_silently=True,
        )

        return user

class CustomTokenObtainSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    confirmation_code = serializers.CharField()