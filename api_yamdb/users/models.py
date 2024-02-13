from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MyUserManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class MyUser(AbstractUser):

    is_moderator = models.BooleanField(
        'Является модератором.',
        default=False,
        help_text=(
            'Атрибут определяет, является ли пользователь модератором, '
            'право удалять и редактировать любые отзывы и комментарии'
        )
    )
    is_admin = models.BooleanField(
        'Является администратором.',
        default=False,
        help_text=(
            'Атрибут определяет, является ли пользователь администратором, '
            'Может создавать и удалять произведения, категории и жанры. '
            'Может назначать роли пользователям.'
        )
    )
    objects = MyUserManager()
