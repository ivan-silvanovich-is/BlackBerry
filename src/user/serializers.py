from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):  # TODO: add an opportunity to change user profile info
    class Meta:
        model = User
        fields = ('date_joined', 'username', 'profile_photo', 'country')
        read_only_fields = fields


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.SlugRelatedField(source='user', slug_field='username', read_only=True)

    class Meta:
        model = UserAddress
        fields = ('created_at', 'user', 'username', 'country', 'region', 'city', 'street', 'house', 'apartment', 'location')
        read_only_fields = ('created_at', )
