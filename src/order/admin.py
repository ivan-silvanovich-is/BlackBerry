from django.contrib import admin

from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'deliverer', 'point', 'total_price', 'created_at', 'delivery_date', 'user_address', 'is_sent')
    list_display_links = ('user',)
    search_fields = ('user__email', 'deliverer__name', 'point__address', 'user_address')


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_details', 'get_price', 'quantity', 'discount')
    list_display_links = ('order', 'product_details')
    search_fields = ('product_details__product__title',)

    def get_price(self, product_obj):
        return product_obj.unit_price / 100

    get_price.short_description = 'Цена за штуку'


@admin.register(Deliverer)
class DelivererAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'get_price')
    list_display_links = ('name', 'phone')
    search_fields = ('name', 'phone')
    prepopulated_fields = {'slug': ('name', )}

    def get_price(self, product_obj):
        return product_obj.delivery_price / 100

    get_price.short_description = 'Цена доставки'


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'location')
    list_display_links = ('address',)
    search_fields = ('address', 'phone', 'location')
