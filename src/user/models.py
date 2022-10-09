from django.db import models
from django.contrib.auth.models import AbstractUser

from config.models import TimeStampMixin, GENDER_CHOICES


__all__ = (
    'User',
    'UserAddress'
)


class User(AbstractUser):
    profile_photo = models.CharField(max_length=100, unique=True, verbose_name='Фото профиля')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    is_active = models.BooleanField(default=False, verbose_name='Активный')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(max_length=256, unique=True, verbose_name='Адрес электронной почты')  # the length is fitted
    country = models.CharField(max_length=50, verbose_name='Страна')
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

    country = models.CharField(max_length=50, verbose_name='Страна')
    region = models.CharField(max_length=50, null=True, blank=True, verbose_name='Регион')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=10, verbose_name='Дом')
    apartment = models.CharField(max_length=10, null=True, blank=True, verbose_name='Квартира')

    location = models.CharField(max_length=22, verbose_name='Местоположение')

    def __str__(self):
        return f'{self.country}, {self.region}, {self.city}, {self.street}, {self.house}, {self.apartment}'

    class Meta:
        verbose_name_plural = 'Адреса пользователей'
        verbose_name = 'Адрес пользователя'
        unique_together = ('user', 'country', 'region', 'city', 'street', 'house', 'apartment', 'location')
        ordering = ['-user']
        get_latest_by = '-created_at'
