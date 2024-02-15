from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import MyUser
from .permissions import IsAdmin
from .serializers import SignUpSerializer, CustomTokenObtainSerializer, UserEditSerializer, UserSerializer


class SignUpView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            MyUser,
            username=serializer.validated_data.get('username')
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation code for Yamdb',
            message=f'Добрый день! Ваш код подтверждения: {confirmation_code}',
            from_email='mail@yamdb.com',
            recipient_list=[serializer.validated_data.get('email')],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(MyUser, username=username)
        if default_token_generator.check_token(
            user,
            confirmation_code
        ):
            token_data = {
                'token': str(AccessToken.for_user(user))
            }
            return Response(token_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    lookup_field = "username"


class UserAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get(self, request):
        user = request.user
        serializer = UserEditSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request):
        user = self.request.user
        serializer = UserEditSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
