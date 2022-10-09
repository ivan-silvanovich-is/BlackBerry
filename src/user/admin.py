from django.contrib import admin

from .models import User, UserAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'full_name', 'gender', 'is_staff', 'is_superuser')
    list_display_links = ('email', 'phone')
    search_fields = ('email', 'phone', 'full_name')


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'region', 'city', 'street', 'house', 'apartment', 'user')
    list_display_links = ('country', 'region', 'city', 'street', 'house', 'apartment')
    search_fields = ('country', 'region', 'city', 'street', 'house', 'apartment', 'user__email')
