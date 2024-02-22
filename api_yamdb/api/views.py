from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,
                                   HTTP_403_FORBIDDEN)

from reviews.models import Title, Review, Category, Genre
from api.serializers import (GenreSerializer, CategorySerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from .filters import TitleFilter
from .permissions import IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


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
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        """Custom patch method."""
        kwargs['partial'] = True
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


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
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        """Custom patch method."""
        kwargs['partial'] = True
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


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
