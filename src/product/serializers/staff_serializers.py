from django.forms.models import model_to_dict
from rest_framework import serializers

from .user_serializers import *
from ..models import *

__all__ = (
    'StaffProductListSerializer',
    'StaffProductItemSerializer',
)


class StaffProductListSerializer(ProductListSerializer):
    class Meta:
        model = Product
        fields = ('created_at', 'updated_at', 'slug', 'category', 'price', 'title', 'discount', 'is_new', 'images')
        read_only_fields = fields


class StaffProductItemSerializer(ProductItemSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    manufacturer = serializers.SlugRelatedField(slug_field='slug', queryset=Manufacturer.objects.all())
    default_color = serializers.SlugRelatedField(slug_field='slug', queryset=Color.objects.all())

    def get_colors_info(self, product):
        product_variations = ProductDetails.objects.filter(product=product)
        product_details = []

        for color_id in product_variations.values_list('product_color', flat=True).distinct():
            color_info = model_to_dict(Color.objects.get(pk=color_id))
            color_info['sizes'] = [
                {
                    'size': obj.product_size.name,
                    'is_stored': obj.quantity,
                } for obj in product_variations.filter(product_color_id=color_id)
            ]

            product_details.append(color_info)

        return product_details

    class Meta:
        model = Product
        fields = '__all__'
