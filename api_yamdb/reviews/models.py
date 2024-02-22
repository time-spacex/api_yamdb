from django.db import models
from django.db.models import (Model, CharField, IntegerField,
                              ManyToManyField, SET_NULL,
                              SlugField, ForeignKey, TextField)

from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import MyUser
from .validators import custom_year_validator


class Category(Model):
    """Category model"""
    name = CharField(max_length=256)
    slug = SlugField(unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Genre(Model):
    """Genre model"""
    name = CharField(max_length=256)
    slug = SlugField(unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Title(Model):
    """Title model"""
    name = CharField(max_length=256)
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
                10,
                message='Оценка не должна превышать 10.'
            ),
            MinValueValidator(
                1,
                message='Оценка не должна быть меньше 1.'
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
        return self.text[:10]


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
        return self.text[:10]
