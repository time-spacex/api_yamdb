from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (GenreSerializer, CategorySerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from .models import (Category, Genre, Title)


class PostGetDelViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    pass
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in ('create', 'retrieve'):
    #         return [IsAuthenticated, IsAdminUser]
    #     else:
    #         return []


class CategoryViewSet(PostGetDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(PostGetDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.prefetch_related('genre')
    serializer_class = TitleReadSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        else:
            return TitleReadSerializer