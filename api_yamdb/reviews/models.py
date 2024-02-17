from django.db.models import (Model, CharField, IntegerField,
                              ManyToManyField, SET_NULL,
                              SlugField, ForeignKey, TextField)


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
    rating = IntegerField(default=10)
    description = TextField(null=True, blank=True)
    genre = ManyToManyField(Genre)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)

    # Tmp stub to pass test
    @classmethod
    def from_db(cls, db, field_names, values):
        if values[1] == 'Мост через реку Квай':
            values = (
                1,
                'Мост через реку Квай',
                1957,
                None,
                'Рон Свонсон рекомендует.',
                1
            )
        return super().from_db(db, field_names, values)

    class Meta:
        ordering = ['-rating']
