from django.core.validators import MinLengthValidator, validate_slug
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import TimeStampMixin, GENDER_CHOICES

__all__ = (
    'User',
    'Address'
)


class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        validators=(MinLengthValidator(1), validate_slug,),
    )
    profile_photo = models.ImageField(
        upload_to='users',
        null=True,
        blank=True,
        unique=True,
        verbose_name='Фото профиля',
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    first_name = models.CharField(max_length=50, verbose_name='Имя', validators=(MinLengthValidator(1),))
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', validators=(MinLengthValidator(1),))
    email = models.EmailField(max_length=256, unique=True, verbose_name='Адрес электронной почты')  # the length is fitted
    country = models.CharField(max_length=50, verbose_name='Страна', validators=(MinLengthValidator(1),))
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')  # the length is fitted

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender', 'country']

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['-date_joined']
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_is_superuser_only_with_is_staff',
                check=~(models.Q(is_staff=False) & models.Q(is_superuser=True)),
            ),
        )


class Address(TimeStampMixin):
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
