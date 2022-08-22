from django.contrib import admin

from .models import User, UserAddress


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'first_name', 'last_name')
    list_display_links = ('email', 'phone')
    search_fields = ('email', 'phone', 'first_name', 'last_name', 'gender')


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'user')
    list_display_links = ('address', )
    search_fields = ('address', 'user__email')


admin.site.register(User, UserAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
