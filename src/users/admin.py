from django.contrib import admin

from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    User.get_full_name.short_description = 'Полное имя'

    list_display = ('email', 'phone', 'get_full_name', 'gender', 'is_staff', 'is_superuser', 'is_active')
    list_display_links = ('email', 'phone')
    search_fields = ('email', 'phone', 'get_full_name')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'region', 'city', 'street', 'house', 'apartment', 'user')
    list_display_links = ('country', 'region', 'city', 'street', 'house', 'apartment')
    search_fields = ('country', 'region', 'city', 'street', 'house', 'apartment', 'user__email')
