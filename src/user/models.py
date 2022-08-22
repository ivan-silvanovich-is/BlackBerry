from django.db import models
from django.contrib.auth.models import AbstractUser

# from werkzeug.security import generate_password_hash, check_password_hash

from config.models import TimeStampMixin, genders_choices


class User(AbstractUser):
    gender = models.CharField(max_length=1, choices=genders_choices, verbose_name='Пол')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(max_length=256, unique=True, verbose_name='Адрес электронной почты')  # max email length = 256
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')  # computed, max phone length = 15

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


# class CustomUser(TimeStampMixin):
#     gender = models.CharField(max_length=1, choices=genders_choices)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=256, null=True, blank=True)  # max email length = 256
#     phone = models.CharField(max_length=20, null=True, blank=True)  # computed, max phone length = 15
#     password = models.CharField(max_length=118)  # computed for pbkdf2:sha256 with salt_length=32
#
#     def set_password_hash(self, password):
#         self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=32)
#
#     def check_password_hash(self, password):
#         return check_password_hash(self.password, password)
#
#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 name="%(app_label)s_%(class)s_email_or_and_phone",
#                 check=(
#                         models.Q(email__isnull=False) | models.Q(phone__isnull=False)
#                 ),
#             )
#         ]
