from django_filters import rest_framework as filters

from config.filters import TimeStampFilter
from config.models import GENDER_CHOICES
from ..models import *

__all__ = (
    'StaffUserFilter',
    'StaffAddressFilter',
)


class StaffUserFilter(filters.FilterSet):
    date_joined = filters.DateTimeFromToRangeFilter()
    last_login = filters.DateTimeFromToRangeFilter()
    is_superuser = filters.BooleanFilter()
    is_staff = filters.BooleanFilter()
    is_active = filters.BooleanFilter()
    gender = filters.ChoiceFilter(choices=GENDER_CHOICES)
    profile_photo = filters.CharFilter(lookup_expr='contains')
    username = filters.CharFilter(lookup_expr='contains')
    first_name = filters.CharFilter(lookup_expr='contains')
    last_name = filters.CharFilter(lookup_expr='contains')
    email = filters.CharFilter(lookup_expr='contains')
    phone = filters.CharFilter(lookup_expr='contains')
    country = filters.CharFilter(lookup_expr='contains')

    order = filters.OrderingFilter(
        fields=(
            ('date_joined', 'date_joined'),
            ('last_login', 'last_login'),
            ('is_superuser', 'is_superuser'),
            ('is_staff', 'is_staff'),
            ('is_active', 'is_active'),
            ('gender', 'gender'),
            ('username', 'username'),
            ('first_name', 'first_name'),
            ('last_name', 'last_name'),
            ('country', 'country'),
        ),
        field_labels={
            'date_joined': 'Дата регистрации',
            'last_login': 'Последний раз в сети',
            'user': 'Пользователь',
            'is_superuser': 'Администратор',
            'is_staff': 'Сотрудник',
            'is_active': 'Активный',
            'gender': 'Пол',
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'country': 'Страна',
        }
    )

    class Meta:
        model = User
        fields = (
            'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'gender', 'profile_photo',
            'username', 'first_name', 'last_name', 'email', 'phone', 'country', 'order',
        )


class StaffAddressFilter(TimeStampFilter):
    user = filters.ModelMultipleChoiceFilter(
        field_name='user__username',
        to_field_name='username',
        queryset=User.objects.all(),
    )
    country = filters.CharFilter(lookup_expr='contains')
    region = filters.CharFilter(lookup_expr='contains')
    city = filters.CharFilter(lookup_expr='contains')
    street = filters.CharFilter(lookup_expr='contains')
    house = filters.CharFilter(lookup_expr='contains')
    apartment = filters.CharFilter(lookup_expr='contains')
    location = filters.CharFilter(lookup_expr='contains')

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('user', 'user'),
            ('country', 'country'),
            ('city', 'city'),
            ('location', 'location'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'user': 'Пользователь',
            'country': 'Страна',
            'city': 'Город',
            'location': 'Местоположение',
        }
    )

    class Meta:
        model = Address
        fields = (
            'created_at', 'updated_at', 'user', 'country', 'region', 'city', 'street', 'house', 'apartment', 'location'
        )
