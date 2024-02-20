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
