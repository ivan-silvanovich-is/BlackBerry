from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    list_display_links = ('name', )
    search_fields = ('name', )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'gender', 'is_new', 'manufacturer', 'get_price')
    list_display_links = ('title', )
    search_fields = ('title', 'description', 'manufacturer')

    def get_price(self, product_obj):
        return product_obj.price / 100

    get_price.short_description = 'Цена'


class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_color', 'product_size', 'stored')
    list_display_links = ('product', )
    search_fields = ('product', )


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'address')
    list_display_links = ('name', )
    search_fields = ('name', 'country', 'address')


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('color', 'color_hex')
    list_display_links = ('color', 'color_hex')
    search_fields = ('color', )


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'product_color')
    list_display_links = ('name', )
    search_fields = ('name', 'product', 'product_color')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'get_rating', 'get_short_text')
    list_display_links = ('user', 'get_short_text')
    search_fields = ('user', 'product', 'text')

    def get_short_text(self, review_obj):
        return review_obj.text[:50] + '...'

    def get_rating(self, review_obj):
        return f'{review_obj.rating} из 10'

    get_short_text.short_description = 'Текст'
    get_rating.short_description = 'Оценка'


class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'user', 'valid_until', 'use_limit', 'used_amount')
    list_display_links = ('name', )
    search_fields = ('name', 'user', 'valid_until')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'deliverer', 'point', 'created_at', 'delivery_date', 'address', 'is_sent')
    list_display_links = ('user', )
    search_fields = ('user__email', 'deliverer__name', 'point__address', 'address')


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_details', 'get_price', 'quantity', 'discount')
    list_display_links = ('order', 'product_details')
    search_fields = ('product_details__product__title', )

    def get_price(self, product_obj):
        return product_obj.unit_price / 100

    get_price.short_description = 'Цена за штуку'


class DelivererAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'get_price')
    list_display_links = ('name', 'phone')
    search_fields = ('name', 'phone')

    def get_price(self, product_obj):
        return product_obj.delivery_price / 100

    get_price.short_description = 'Цена доставки'


class PointAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'location')
    list_display_links = ('address', )
    search_fields = ('address', 'phone', 'location')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetails, ProductDetailsAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize)
admin.site.register(ProductMaterial)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(Deliverer, DelivererAdmin)
admin.site.register(Point, PointAdmin)
