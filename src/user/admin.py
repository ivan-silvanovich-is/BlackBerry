from django.contrib import admin

from .models import User, UserAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'full_name', 'gender', 'is_staff')
    list_display_links = ('email', 'phone')
    search_fields = ('email', 'phone', 'full_name')


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'user')
    list_display_links = ('address', )
    search_fields = ('address', 'user__email')
