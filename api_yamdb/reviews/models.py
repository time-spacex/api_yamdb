from django.db import models
from django.db.models import (Model, CharField,
                              ManyToManyField, SET_NULL,
                              SlugField, ForeignKey, TextField)

from django.core.validators import MaxValueValidator, MinValueValidator

from api_yamdb.settings import (
    MAX_CHARFIELD_LENGTH,
    MAX_RATING_SCORE_VALUE,
    MAX_STRING_REPRESENTATION_LENGTH,
    MIN_RATING_SCORE_VALUE
)
from users.models import MyUser
from .validators import custom_year_validator


class Category(Model):
    """Category model"""
    name = CharField(max_length=MAX_CHARFIELD_LENGTH)
    slug = SlugField(unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Genre(Model):
    """Genre model"""
    name = CharField(max_length=MAX_CHARFIELD_LENGTH)
    slug = SlugField(unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Title(Model):
    """Title model"""
    name = CharField(max_length=MAX_CHARFIELD_LENGTH)
    year = models.SmallIntegerField(validators=[custom_year_validator])
    description = TextField(blank=True)
    genre = ManyToManyField(Genre)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)


class Review(models.Model):
    """Review Model."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка произведения',
        validators=[
            MaxValueValidator(
                MAX_RATING_SCORE_VALUE,
                message=(
                    'Оценка не должна '
                    f'превышать {MAX_RATING_SCORE_VALUE}.'
                )
            ),
            MinValueValidator(
                MIN_RATING_SCORE_VALUE,
                message=(
                    'Оценка не должна '
                    f'быть меньше {MIN_RATING_SCORE_VALUE}.'
                )
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author_unique'
            ),
        ]

    def __str__(self):
        return self.text[:MAX_STRING_REPRESENTATION_LENGTH]


class Comment(models.Model):
    """Comment Model."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:MAX_STRING_REPRESENTATION_LENGTH]
