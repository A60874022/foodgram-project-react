from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс для работы с модель """
    email = models.EmailField('email address', max_length=254, blank=True)
    first_name = models.CharField('first name', max_length=150, blank=True)
    password = models.CharField(
        blank=True,
        max_length=150
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на данного пользователя',
        help_text='Отметьте для подписки на данного пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.username
