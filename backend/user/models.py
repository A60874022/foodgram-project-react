from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс для работы с модель """
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Уникальное имя',
        validators=[AbstractUser.username_validator, ],)
    password = models.CharField(max_length=150)
    email = models.EmailField('электронный адрес', max_length=254)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.username