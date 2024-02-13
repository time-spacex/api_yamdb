from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import MyUser
from .serializers import UserSerializer, CustomTokenObtainSerializer


class SignUpView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get('confirmation_code')
            user = get_object_or_404(MyUser, username=username)
            if user and user.confirmation_code == confirmation_code:
                token_data = {
                    'token': RefreshToken.for_user(user).access_token.get('jti')
                }
                return Response(token_data, status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed('Invalid username or confirmation code')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
