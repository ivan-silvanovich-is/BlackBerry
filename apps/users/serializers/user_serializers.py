from rest_framework import serializers

from ..models import *

__all__ = (
    'PublicUserSerializer',
    'PrivateUserSerializer',
    'AddressSerializer',
)


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('date_joined', 'username', 'profile_photo', 'country')
        read_only_fields = fields


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'date_joined', 'last_login', 'username', 'first_name', 'last_name', 'email', 'phone', 'profile_photo',
            'gender', 'country'
        )
        read_only_fields = ('date_joined', 'last_login', 'email')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Address
        fields = (
            'created_at', 'user', 'country', 'region', 'city', 'street', 'house', 'apartment', 'location'
        )
        read_only_fields = ('created_at',)
