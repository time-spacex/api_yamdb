from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,
                                   HTTP_403_FORBIDDEN)

from .serializers import (GenreSerializer, CategorySerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from .models import (Category, Genre, Title)


class PostGetDelUpdViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           mixins.UpdateModelMixin,
                           GenericViewSet):

    def update(self, request, *args, **kwargs):
        if (self.check_forbidden_roles(request)):
            return Response(status=HTTP_403_FORBIDDEN)
        return super().update(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        if (self.check_forbidden_roles(request)):
            return Response(status=HTTP_403_FORBIDDEN)
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        if (self.check_forbidden_roles(request)):
            return Response(status=HTTP_403_FORBIDDEN)
        return super().destroy(request, args, kwargs)

    def check_forbidden_roles(self, request):
        if (hasattr(request.user, 'role') and
                request.user.role in ['user', 'moderator']):
            return True
        else:
            return False

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('create', 'destroy', 'update', 'partial_update'):
            return [IsAuthenticated()]
        else:
            return []


class CategoryViewSet(PostGetDelUpdViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(PostGetDelUpdViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(PostGetDelUpdViewSet):
    serializer_class = TitleReadSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        else:
            return TitleReadSerializer

    def get_queryset(self):
        genre_slug = self.request.query_params.get('genre', None)
        category_slug = self.request.query_params.get('category', None)
        queryset = Title.objects.prefetch_related('genre')
        if genre_slug:
            queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset.fitler(category__slug=category_slug)
        return queryset.all()
