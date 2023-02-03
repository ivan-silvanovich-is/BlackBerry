from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from ..models import *

__all__ = (
    'AdminUserSerializer',
)


class AdminUserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(allow_null=True, default=None, label='Фото профиля', max_length=100, required=False, validators=[UniqueValidator(queryset=User.objects.all()),])

    def validate_is_superuser(self, is_superuser):
        message = 'Пользователь не может быть администратором, если он не является сотрудником.'
        data = self.get_initial()

        if is_superuser and not data['is_staff']:
            raise ValidationError(message, code='constraint')

        return is_superuser

    class Meta:
        model = User
        fields = (
            'id', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'username', 'password',
            'first_name', 'last_name', 'gender', 'profile_photo', 'email', 'phone', 'country', 'groups',
            'user_permissions',
        )
