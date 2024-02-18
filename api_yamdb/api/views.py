from django.db.models import Avg
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from reviews.models import Title, Review
from .permissions import (
    IsAdminModeratorAuthorOrReadOnly,
)
from .serializers import (
    CommentSerializer, ReviewSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,
                                   HTTP_403_FORBIDDEN)

from api.serializers import (GenreSerializer, CategorySerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from reviews.models import (Category, Genre, Title)


def check_forbidden_roles(request):
    """Forbidden for user and moderator roles."""
    if (hasattr(request.user, 'role') and
            request.user.role in ['user', 'moderator']):
        return Response(status=HTTP_403_FORBIDDEN)
    else:
        return None


def check_not_allowed_roles(request, not_allowed_roles):
    """Not allowed method for not allowed roles."""
    if (hasattr(request.user, 'role') and
            request.user.role in not_allowed_roles):
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return None


class PostGetDelUpdViewSet(ModelViewSet):
    """Post Get Delete Update View Set."""

    def update(self, request, *args, **kwargs):
        """Checks not allowed roles, forbiden roles and perform update."""
        not_allowed = check_not_allowed_roles(request, ['admin'])
        if not_allowed:
            return not_allowed
        forbidden = check_forbidden_roles(request)
        if forbidden:
            return forbidden
        return super().update(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """Create method."""
        forbidden = check_forbidden_roles(request)
        if forbidden:
            return forbidden
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete method."""
        forbidden = check_forbidden_roles(request)
        if forbidden:
            return forbidden
        return super().destroy(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Get method."""
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires depending on action.
        """
        if self.action in ('create', 'destroy', 'update', 'partial_update'):
            return [IsAuthenticated()]
        else:
            return []

class CategoryViewSet(PostGetDelUpdViewSet):
    """Category view set."""
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(PostGetDelUpdViewSet):
    """Genre View Set."""
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    """Title View Set."""
    serializer_class = TitleReadSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')

    def get_serializer_class(self):
        """Getting Serializer Class."""
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        else:
            return TitleReadSerializer

    def get_queryset(self):
        """Get queryset."""
        genre_slug = self.request.query_params.get('genre', None)
        category_slug = self.request.query_params.get('category', None)
        queryset = Title.objects.prefetch_related('genre')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return (queryset
                .annotate(rating=Round(Avg('reviews__score')))
                .all())

    def get_permissions(self):
        """Get permissions."""
        if self.action in ('create', 'destroy', 'update', 'partial_update'):
            return [IsAuthenticated()]
        else:
            return []

    def create(self, request, *args, **kwargs):
        """Create method."""
        forbidden = check_forbidden_roles(request)
        if forbidden:
            return forbidden
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """Destroy method."""
        forbidden = check_forbidden_roles(request)
        if forbidden:
            return forbidden
        return super().destroy(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        """Update method."""
        if 'partial' not in kwargs:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
        if (hasattr(request.user, 'role') and
                request.user.role in ['admin']):
            return super().update(request, *args, **kwargs)
        forbidden = check_forbidden_roles(request)
        if forbidden:
            return forbidden
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


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
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Gets all the comments of the specific review."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Saves the author of the comment as authenticated user."""
        serializer.save(author=self.request.user, review=self.get_review())
