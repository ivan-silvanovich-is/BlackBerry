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
    list_display = ('product', 'color', 'size', 'quantity')
    list_display_links = ('product',)
    search_fields = ('product',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'address')
    list_display_links = ('name',)
    search_fields = ('name', 'country', 'address')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex')
    list_display_links = ('name', 'hex')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('get_image_path', 'product', 'color')
    list_display_links = ('get_image_path',)
    search_fields = ('name', 'product__title', 'color__name')

    def get_image_path(self, image_obj):
        return image_obj.path.path

    get_image_path.short_description = 'Путь к картинке'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'get_rating', 'get_short_text')
    list_display_links = ('user', 'get_short_text')
    search_fields = ('user__username', 'product__title', 'text')

    def get_short_text(self, review_obj):
        return review_obj.text[:50] + '...'

    def get_rating(self, review_obj):
        return f'{review_obj.rating} из 10'

    get_short_text.short_description = 'Текст'
    get_rating.short_description = 'Оценка'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'discount', 'user', 'valid_until', 'use_limit', 'used_amount')
    list_display_links = ('name',)
    search_fields = ('name', 'user__username', 'valid_until')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('material', 'product', 'part')
    list_display_links = ('material', 'product')
    search_fields = ('material__name', 'product__title')


admin.site.register(Size)
