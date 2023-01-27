from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from .user_serializers import *
from ..models import *

__all__ = (
    'StaffCategorySerializer',
    'StaffProductListSerializer',
    'StaffProductItemSerializer',
    'StaffProductDetailsSerializer',
    'StaffManufacturerSerializer',
    'StaffMaterialSerializer',
    'StaffProductMaterialSerializer',
    'StaffColorSerializer',
    'StaffSizeSerializer',
    'StaffImageSerializer',
    'StaffReviewSerializer',
    'StaffCouponSerializer',
)


class StaffCategorySerializer(CategorySerializer):
    parent_category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Category
        fields = ('id', 'created_at', 'updated_at', 'parent_category', 'child_categories', 'name', 'slug', 'logo')


class StaffProductListSerializer(ProductListSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'created_at', 'updated_at', 'slug', 'category', 'price', 'title', 'discount', 'is_new', 'images'
        )


class StaffProductItemSerializer(ProductItemSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    manufacturer = serializers.SlugRelatedField(slug_field='slug', queryset=Manufacturer.objects.all())
    default_color = serializers.SlugRelatedField(slug_field='slug', queryset=Color.objects.all())

    def get_colors_info(self, product):
        product_variations = ProductDetails.objects.filter(product=product)
        product_details = []

        for color_id in product_variations.values_list('color', flat=True).distinct():
            color_info = model_to_dict(Color.objects.get(pk=color_id))
            color_info['sizes'] = [
                {
                    'size': obj.size.path,
                    'is_stored': obj.quantity,
                } for obj in product_variations.filter(color_id=color_id)
            ]

            product_details.append(color_info)

        return product_details

    class Meta:
        model = Product
        fields = (
            'id', 'created_at', 'updated_at', 'default_color', 'colors', 'category', 'manufacturer', 'is_new',
            'gender', 'title', 'slug', 'description', 'price', 'discount'
        )


class StaffProductDetailsSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=Product.objects.all())
    color = serializers.SlugRelatedField(slug_field='slug', queryset=Color.objects.all())
    size = serializers.SlugRelatedField(slug_field='name', queryset=Size.objects.all())

    class Meta:
        model = ProductDetails
        fields = ('id', 'created_at', 'updated_at', 'product', 'color', 'size', 'quantity')


class StaffManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class StaffMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'slug')


class StaffProductMaterialSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=Product.objects.all())
    material = serializers.SlugRelatedField(slug_field='slug', queryset=Material.objects.all())

    class Meta:
        model = ProductMaterial
        fields = '__all__'


class StaffColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class StaffSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class StaffImageSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=Product.objects.all())
    color = serializers.SlugRelatedField(slug_field='slug', queryset=Color.objects.all())

    class Meta:
        model = Image
        fields = ('id', 'created_at', 'updated_at', 'product', 'color', 'path')


class StaffReviewSerializer(ReviewSerializer):
    class Meta:
        model = Review
        fields = ('id', 'created_at', 'updated_at', 'user', 'product', 'rating', 'text')


class StaffCouponSerializer(CouponSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), allow_null=True)

    categories = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Category.objects.all(),
    )

    def validate_used_amount(self, used_amount):
        message = 'Количество использований не может превышать лимит использований.'
        data = self.get_initial()

        if used_amount > int(data['use_limit']):
            raise ValidationError(message, code='constraint')

    class Meta:
        model = Coupon
        fields = (
            'id', 'created_at', 'updated_at', 'name', 'slug', 'is_active', 'user', 'discount', 'categories',
            'valid_until', 'use_limit', 'used_amount'
        )
