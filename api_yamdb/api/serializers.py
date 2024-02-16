from rest_framework.serializers import ModelSerializer, SlugRelatedField

from reviews.models import Category, Genre, Title


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWriteSerializer(ModelSerializer):
    """Title Write serializer."""
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genre.objects.all())
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')