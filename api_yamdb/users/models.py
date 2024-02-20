from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, CheckConstraint


class MyUser(AbstractUser):
    """Custom User model class."""

    ROLE_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
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

        constraints = [
            CheckConstraint(
                check=~Q(username__iexact='me'),
                name='Username me is not valid'
            )
        ]
