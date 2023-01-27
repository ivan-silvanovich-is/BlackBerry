from rest_framework import serializers

from .user_serializers import AddressSerializer
from ..models import *

__all__ = (
    'StaffUserSerializer',
    'StaffAddressSerializer',
)


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'username', 'password',
            'first_name', 'last_name', 'gender', 'profile_photo', 'email', 'phone', 'country',
        )
        read_only_fields = (
            'id', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'username', 'password',
            'first_name', 'last_name', 'gender', 'profile_photo', 'email', 'phone', 'country',
        )


class StaffAddressSerializer(AddressSerializer):
    class Meta:
        model = Address
        fields = (
            'id', 'created_at', 'updated_at', 'user', 'country', 'region', 'city', 'street', 'house',
            'apartment', 'location',
        )
