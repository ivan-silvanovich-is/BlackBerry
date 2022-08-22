from django.db import models
from django.contrib.auth.models import AbstractUser

from config.models import TimeStampMixin, GENDER_CHOICES


class User(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(max_length=256, unique=True, verbose_name='Адрес электронной почты')  # the length is fitted
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')  # the length is fitted

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    full_name.fget.short_description = 'Полное имя'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender']

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['-date_joined']


class UserAddress(TimeStampMixin):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    class Meta:
        verbose_name_plural = 'Адреса пользователей'
        verbose_name = 'Адрес пользователя'
        unique_together = ['user', 'address']
        ordering = ['-user']
        get_latest_by = '-created_at'
