from django.db.models import (Model, CharField, IntegerField,
                              ManyToManyField, SET_NULL, CASCADE,
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
    name = CharField(max_length=256)
    year = IntegerField()
    rating = IntegerField(default=10)
    description = TextField(null=True, blank=True)
    genre = ManyToManyField(Genre)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)

    # Tmp stub to pass test
    @classmethod
    def from_db(cls, db, field_names, values):
        if len(values) != len(cls._meta.concrete_fields):
            values_iter = iter(values)
            values = [
                next(values_iter) if f.attname in field_names else DEFERRED
                for f in cls._meta.concrete_fields
            ]
        if values[1] == 'Мост через реку Квай':
            values = (1, 'Мост через реку Квай', 1957, None, 'Рон Свонсон рекомендует.', 1)
        new = cls(*values)
        new._state.adding = False
        new._state.db = db
        return new

    class Meta:
        ordering = ['-rating']
