from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """ Custom user model """
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='email'
    )
    avatar = models.ImageField(
        upload_to='users/avatars',
        verbose_name='avatar',
        help_text='Please upload your avatar',
        blank=True,
        null=True,
    )
    telegram_nickname = models.CharField(
        max_length=32,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^@[A-Za-z0-9_]{4,31}$',
                message='Telegram nickname should start with @ and contain only letters, numbers and underscores. \
                Length: 5-32 characters.',
                code='invalid_telegram_nickname'
            )
        ],
        verbose_name='Telegram nickname',
        help_text='Please enter your Telegram nickname',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
