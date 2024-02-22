from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Title, Comment


class CategorySerializer(ModelSerializer):
    """Category serializer."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(ModelSerializer):
    """Genre Serializer."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(ModelSerializer):
    """Title Read Serializer."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        required=False
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWriteSerializer(ModelSerializer):
    """Title Write serializer."""
    rating = serializers.IntegerField(
        read_only=True, allow_null=True
    )
    genre = SlugRelatedField(slug_field='slug', many=True,  
                             queryset=Genre.objects.all())
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    
    def to_representation(self, instance):
        """Customize serializer data for 'genre' and 'category' fields."""
        ret = super().to_representation(instance)
        ret['genre'] = []
        for item in instance.genre.values():
            genre_data = {}
            genre_data['name'] = item.get('name')
            genre_data['slug'] = item.get('slug')
            ret['genre'].append(genre_data)
        ret['category'] = {}
        ret['category']['name'] = instance.category.name
        ret['category']['slug'] = instance.category.slug
        return ret
    
    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError("Genre cannot be empty.")
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class ReviewSerializer(ModelSerializer):
    """Review serializer."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        """
        Validation method to make sure the author
        has not left the review for this object.
        """
        if self.context['request'].method == 'POST':
            title = get_object_or_404(
                Title, pk=self.context['view'].kwargs.get('title_id')
            )
            author = self.context['request'].user
            if Review.objects.filter(title_id=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data


class CommentSerializer(ModelSerializer):
    """Comment serializer."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
