from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'gender', 'is_new', 'manufacturer', 'get_price')
    list_display_links = ('title',)
    search_fields = ('title', 'description', 'manufacturer__name')
    prepopulated_fields = {'slug': ('title', )}

    def get_price(self, product_obj):
        return product_obj.price / 100

    get_price.short_description = 'Цена'


@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_color', 'product_size', 'stored')
    list_display_links = ('product',)
    search_fields = ('product',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'address')
    list_display_links = ('name',)
    search_fields = ('name', 'country', 'address')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex')
    list_display_links = ('name', 'hex')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name', )}


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'product_color')
    list_display_links = ('name',)
    search_fields = ('name', 'product', 'product_color')


@admin.register(Review)
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


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'user', 'valid_until', 'use_limit', 'used_amount')
    list_display_links = ('name',)
    search_fields = ('name', 'user', 'valid_until')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'deliverer', 'point', 'total_price', 'created_at', 'delivery_date', 'address', 'is_sent')
    list_display_links = ('user',)
    search_fields = ('user__email', 'deliverer__name', 'point__address', 'address')


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

    def get_price(self, product_obj):
        return product_obj.delivery_price / 100

    get_price.short_description = 'Цена доставки'


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'location')
    list_display_links = ('address',)
    search_fields = ('address', 'phone', 'location')


@admin.register(ProductMaterialProduct)
class ProductMaterialProductAdmin(admin.ModelAdmin):
    list_display = ('product_material', 'product', 'part')
    list_display_links = ('product_material', 'product')
    search_fields = ('product_material__name', 'product__title')


admin.site.register(ProductSize)
