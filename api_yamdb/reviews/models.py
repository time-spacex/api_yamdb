from django.db import models

from .validators import validate_score
from django.db.models import (Model, CharField, IntegerField,
                              ManyToManyField, SET_NULL, CASCADE,
                              SlugField, ForeignKey, TextField)
from users.models import MyUser


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
    year = IntegerField()
    description = TextField(null=True, blank=True)
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
        validators=[validate_score]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:10]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author_unique'
            ),
        ]


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
