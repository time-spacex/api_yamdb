from django.db.models import (Model, CharField, IntegerField,
                              ManyToManyField, SET_NULL,
                              SlugField, ForeignKey, TextField)


class Category(Model):
    name = CharField(max_length=256)
    slug = SlugField(unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Genre(Model):
    name = CharField(max_length=256)
    slug = SlugField(unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Title(Model):
    name = CharField(max_length=512)
    year = IntegerField()
    rating = IntegerField()
    description = TextField(null=True, blank=True)
    genre = ManyToManyField(Genre)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)

    class Meta:
        ordering = ['-rating']
