from rest_framework import serializers

from products.serializers.user_serializers import ProductDetailsSerializer
from ..models import *

__all__ = (
    'OrderSerializer',
    'DelivererSerializer',
    'PointSerializer',
)


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer(source='product_details')

    class Meta:
        model = OrderDetails
        fields = ('product', 'unit_price', 'quantity', 'discount')
        read_only_fields = ('unit_price', 'quantity', 'discount')


class OrderSerializer(serializers.ModelSerializer):  # TODO: add an opportunity to add and update orders
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_details = OrderDetailsSerializer(many=True)
    deliverer = serializers.SlugRelatedField(
        slug_field='slug',
        allow_null=True,
        queryset=Deliverer.objects.all(),
        label='Доставщик'
    )

    class Meta:
        model = Order
        fields = ('id', 'user', 'point', 'deliverer', 'address', 'delivery_date', 'order_details', 'delivery_price', 'total_price', 'is_sent')
        read_only_fields = ('id', 'delivery_date', 'delivery_price', 'total_price', 'is_sent')


class DelivererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverer
        fields = ('name', 'slug', 'delivery_price')
        read_only_fields = fields


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('phone', 'address', 'location')
        read_only_fields = fields
