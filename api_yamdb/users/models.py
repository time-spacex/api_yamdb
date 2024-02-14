from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
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
        default=USER
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
        null=True,
    )

    confirmation_code = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
    
        constraints = [
            CheckConstraint(
                check=~Q(username__iexact='me'),
                name='Username me is not valid'
            )
        ]
