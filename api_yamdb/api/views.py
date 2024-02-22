from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title, Review, Category, Genre
from users.models import MyUser
from .filters import TitleFilter
from .permissions import (
    IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly, IsAdmin
)
from .serializers import (
    SignUpSerializer,
    CustomTokenObtainSerializer,
    UserEditSerializer,
    UserSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class SignUpView(APIView):
    """View class for registering users."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Method of processing 'post' request when registering users."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainView(APIView):
    """Custom view class for receiving a token."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Method of processing 'post' request when receiving a token."""
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get(
            'confirmation_code'
        )
        user = get_object_or_404(MyUser, username=username)
        if not default_token_generator.check_token(
            user,
            confirmation_code
        ):
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        token_data = {
            'token': str(AccessToken.for_user(user))
        }
        return Response(token_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for receiving and editing user data."""

    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
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


class CategoryViewSet(ModelViewSet):
    """Category view set."""
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def retrieve(self, request, *args, **kwargs):
        """Custom get method."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        """Custom patch method."""
        kwargs['partial'] = True
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(ModelViewSet):
    """Genre View Set."""
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        """Custom get method."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        """Custom put and patch method."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(ModelViewSet):
    """Title View Set."""
    serializer_class = TitleReadSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        """Getting Serializer Class."""
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        else:
            return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Review View Set."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination
    ordering = ('-pub_date',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        """Gets the title of the review."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Gets all the reviews of the specific title."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Saves the author of the review as authenticated user."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Comment View Set."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination
    ordering = ('-pub_date',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """Gets the review of the comment."""
        return get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        """Gets all the comments of the specific review."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Saves the author of the comment as authenticated user."""
        serializer.save(author=self.request.user, review=self.get_review())
