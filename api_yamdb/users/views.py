from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import MyUser
from .permissions import IsAdmin
from .serializers import (
    SignUpSerializer,
    CustomTokenObtainSerializer,
    UserEditSerializer,
    UserSerializer
)


class SignUpView(APIView):
    """View class for registering users."""

    permission_classes = (permissions.AllowAny,)

    def send_email(self, email, confirmation_code):
        """Method for sending email."""
        send_mail(
            subject='Confirmation code for Yamdb',
            message=f'Добрый день! Ваш код подтверждения: {confirmation_code}',
            from_email='mail@yamdb.com',
            recipient_list=[email],
            fail_silently=True
        )

    def post(self, request):
        """Method of processing 'post' request when registering users."""
        serializer = SignUpSerializer(data=request.data)
        username = serializer.initial_data.get('username')
        email = serializer.initial_data.get('email')
        users = MyUser.objects.all()
        if serializer.is_valid():
            try:
                users.get(username=username, email=email)
                user = get_object_or_404(
                    MyUser,
                    username=username
                )
                confirmation_code = default_token_generator.make_token(user)
                self.send_email(email, confirmation_code)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except MyUser.DoesNotExist:
                serializer.save()
                user = get_object_or_404(
                    MyUser,
                    username=username
                )
                confirmation_code = default_token_generator.make_token(user)
                self.send_email(email, confirmation_code)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom view class for receiving a token."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Method of processing 'post' request when receiving a token."""
        serializer = CustomTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
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
    """Viewset for receiving and editing user data."""

    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
        url_name='me'
    )
    def user_me_get_and_patch(self, request):
        user = self.request.user
        serializer = UserEditSerializer(user)
        if self.request.method == 'PATCH':
            serializer = UserEditSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


'''class UserMeAPIView(APIView):
    """View class for receiving and editing data about your profile."""

    queryset = MyUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Method of processing 'get' request."""
        user = request.user
        serializer = UserEditSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Method of processing 'patch' request."""
        user = self.request.user
        serializer = UserEditSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
