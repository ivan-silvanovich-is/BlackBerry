from rest_framework import serializers

from .models import *
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "name", "logo", "description", "country")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("name", )


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Review
        fields = ("created_at", "user", "rating", "text")


class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')

    def get_images(self, product):
        qs = ProductImage.objects.filter(product=product, product_color=product.default_color)
        serializer = ProductImageSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = ("id", 'price', 'title', 'discount', 'is_new', 'images')


class ProductItemSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    colors = serializers.SerializerMethodField(method_name='get_colors_info')
    materials = serializers.SerializerMethodField(method_name='get_materials')
    bread_crumbs = serializers.SerializerMethodField(method_name='get_bread_crumbs')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')

    def get_colors_info(self, product):
        product_variations = ProductDetails.objects.filter(product=product)
        product_details = []

        for color_id in product_variations.values_list('product_color', flat=True).distinct():
            color = ProductColor.objects.get(pk=color_id)
            product_details.append({
                'id': color.pk,
                'name': color.name,
                'hex': color.hex,
                'sizes': [
                    {
                        'size': obj.product_size.name,
                        'is_stored': bool(obj.stored),
                    } for obj in product_variations.filter(product_color=color)
                ]
            })

        return product_details

    def get_materials(self, product):
        data = []
        for obj in ProductMaterialProduct.objects.filter(product=product):
            data.append({
                "id": obj.pk,
                "material": obj.product_material.name,
                "part": obj.part
            })
        return data

    def get_bread_crumbs(self, product):
        bread_crumbs_list = []
        category = product.category

        while category:
            bread_crumbs_list.insert(0, CategorySerializer(category).data)
            category = category.parent_category

        return bread_crumbs_list

    def get_reviews(self, product):
        serializer = ProductReviewSerializer(instance=Review.objects.filter(product=product), many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = ('id', 'manufacturer', 'category', 'bread_crumbs', 'default_color', 'colors', 'is_new', 'gender',
                  'title', 'description', 'materials', 'price', 'discount', 'reviews')
