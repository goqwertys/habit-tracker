from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


NULLABLE = {
    'blank': True,
    'null': True
}


class UserManager(BaseUserManager):
    """ Custom user model manager where email is the unique identifiers for authentication """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ Create and save superuser with the given email, password and telegram nickname """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be is_superuser=True')

        return self.create_user(email, password, **extra_fields)


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
        **NULLABLE
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
        **NULLABLE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
