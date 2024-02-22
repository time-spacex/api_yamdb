from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Title, Comment

from api_yamdb.settings import MAX_USERNAME_LENGTH
from users.validators import not_equal_me_username_validator
from users.models import MyUser


class SignUpSerializer(serializers.Serializer):
    """Serializer for user registration."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
        validators=[
            UnicodeUsernameValidator(),
            not_equal_me_username_validator
        ]
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        """
        Validation method for checking existing users' input into data fields.
        """
        user_with_email_exists = MyUser.objects.filter(
            email=data.get('email')
        ).first()
        user_with_username_exists = MyUser.objects.filter(
            username=data.get('username')
        ).first()
        if user_with_email_exists != user_with_username_exists:
            error_msg = {}
            if user_with_email_exists:
                error_msg['email'] = (
                    'Пользователь с таким email уже существует'
                )
            if user_with_username_exists:
                error_msg['username'] = (
                    'Пользователь с таким username уже существует'
                )
            raise serializers.ValidationError(
                error_msg, code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def send_email(self, email, confirmation_code):
        """Method for sending email."""
        send_mail(
            subject='Confirmation code for Yamdb',
            message=f'Добрый день! Ваш код подтверждения: {confirmation_code}',
            from_email='mail@yamdb.com',
            recipient_list=[email],
            fail_silently=True
        )

    def create(self, validated_data):
        """
        Create and return a new `MyUser` instance, given the validated data,
        send confirmation code on email.
        """
        username = self.initial_data.get('username')
        email = self.initial_data.get('email')
        user, created = MyUser.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        self.send_email(email, confirmation_code)
        return user


class CustomTokenObtainSerializer(serializers.Serializer):
    """Serializer to get a token."""

    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator, not_equal_me_username_validator]
    )
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for receiving and editing user data."""

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserEditSerializer(UserSerializer):
    """Serializer for receiving and editing data about your profile."""

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


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
            raise serializers.ValidationError(
                'Поле "genre" не должно быть пустым.'
            )
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
