from django.forms.models import model_to_dict
from rest_framework import serializers

from ..models import *

__all__ = (
    'CategorySerializer',
    'ProductListSerializer',
    'ProductItemSerializer',
    'ManufacturerSerializer',
    'MaterialSerializer',
    'ProductMaterialSerializer',
    'ColorSerializer',
    'SizeSerializer',
    'ImageSerializer',
    'ReviewSerializer',
    'CouponSerializer',
)


class CategorySerializer(serializers.ModelSerializer):
    child_categories = serializers.SerializerMethodField(method_name="get_child_categories")

    def get_child_categories(self, category):
        if not category.child_categories.exists():
            return []

        child_categories = []
        for child_category in category.child_categories.all():
            category = model_to_dict(child_category, fields=('slug', 'name'))
            category['child_categories'] = self.get_child_categories(child_category)
            child_categories.append(category)

        return child_categories

    class Meta:
        model = Category
        fields = ('slug', 'name', 'child_categories')
        read_only_fields = fields


class ProductListSerializer(serializers.ModelSerializer):  # TODO: find better way to extract images for product
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    images = serializers.SerializerMethodField(method_name='get_images')

    def get_images(self, product):
        return product.images.filter(color=product.default_color).values('name')

    class Meta:
        model = Product
        fields = ('slug', 'category', 'price', 'title', 'discount', 'is_new', 'images')
        read_only_fields = fields


class ProductItemSerializer(serializers.ModelSerializer):
    default_color = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    colors = serializers.SerializerMethodField(method_name='get_colors_info')

    def get_colors_info(self, product):
        product_variations = ProductDetails.objects.filter(product=product)
        product_details = []

        for color_id in product_variations.values_list('color', flat=True).distinct():
            color_info = model_to_dict(Color.objects.get(pk=color_id))
            color_info['sizes'] = [
                {
                    'size': obj.size.name,
                    'is_stored': bool(obj.quantity),
                } for obj in product_variations.filter(color_id=color_id)
            ]

            product_details.append(color_info)

        return product_details

    class Meta:
        model = Product
        fields = ('slug', 'default_color', 'colors', 'is_new', 'gender', 'title', 'description', 'price', 'discount')
        read_only_fields = fields


class ProductDetailsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(source='product', slug_field='slug', read_only=True)
    color = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    size = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ProductDetails
        fields = ('slug', 'color', 'size')


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("slug", "name", "logo", "description", "country", "address")
        read_only_fields = fields


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('name', 'slug')
        read_only_fields = fields


class ProductMaterialSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    material = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = ProductMaterial
        fields = ('product', 'material', 'part')
        read_only_fields = fields


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('slug', 'name', 'hex')
        read_only_fields = fields


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('name', )


class ImageSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    color = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Image
        fields = ('product', 'color', 'name')
        read_only_fields = fields


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.SlugRelatedField(source='user', slug_field='username', read_only=True)
    product = serializers.SlugRelatedField(slug_field='slug', queryset=Product.objects.all(), label='Продукт')

    class Meta:
        model = Review
        fields = ('created_at', 'user', 'username', 'product', 'rating', 'text')
        read_only_fields = ('created_at', 'username')


class CouponSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Coupon
        fields = ('name', 'slug', 'discount', 'valid_until', 'categories')
        read_only_fields = fields
