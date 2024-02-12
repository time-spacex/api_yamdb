from django.db.models import (Model, CharField, IntegerField,
                              ManyToManyField, SET_NULL,
                              SlugField, ForeignKey, TextField)


class Category(Model):
    name = CharField(max_length=256)
    slug = SlugField(max_length=50)


class Genre(Model):
    name = CharField(max_length=256)
    slug = SlugField(max_length=50)


class Title(Model):
    name = CharField(max_length=512)
    year = IntegerField()
    rating = IntegerField()
    description = TextField()
    genre = ManyToManyField(Genre)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)
