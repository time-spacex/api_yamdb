from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

from api_yamdb.settings import MAX_USERNAME_LENGTH
from .validators import not_equal_me_username_validator


class MyUser(AbstractUser):
    """Custom User model class."""

    ROLE_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            not_equal_me_username_validator
        ]
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff
