from django_filters import rest_framework as filters

from config.models import GENDER_CHOICES
from user.models import User
from .models import *


__all__ = (
    'CategoryFilter',
    'ProductFilter',
    'ProductMaterialFilter',
    'ManufacturerFilter',
    'ProductImageFilter',
    'ReviewFilter',
)


class CategoryFilter(filters.FilterSet):
    parent_category = filters.ModelMultipleChoiceFilter(
        field_name='parent_category',
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    child_category = filters.ModelMultipleChoiceFilter(
        field_name='child_categories__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Category
        fields = ('parent_category', 'child_category')


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()
    manufacturer = filters.CharFilter(field_name="manufacturer__slug", lookup_expr="exact")
    category = filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    gender = filters.ChoiceFilter(choices=GENDER_CHOICES)

    material = filters.ModelMultipleChoiceFilter(
        field_name="materials__slug",
        to_field_name="slug",
        queryset=ProductMaterial.objects.all()
    )
    color = filters.ModelMultipleChoiceFilter(
        field_name="details__product_color__slug",
        to_field_name="slug",
        queryset=ProductColor.objects.all()
    )
    size = filters.ModelMultipleChoiceFilter(
        field_name="details__product_size__name",
        to_field_name="name",
        queryset=ProductSize.objects.all()
    )

    class Meta:
        model = Product
        fields = ('price', 'manufacturer', 'category', 'gender', 'material', 'color', 'size')


class ManufacturerFilter(filters.FilterSet):
    manufacturer = filters.AllValuesMultipleFilter(field_name="slug", label="Производитель")
    country = filters.AllValuesMultipleFilter(field_name="country", label="Страна")

    class Meta:
        model = Manufacturer
        fields = ('manufacturer', 'country')


class ProductMaterialFilter(filters.FilterSet):
    material = filters.ModelMultipleChoiceFilter(
        field_name="product_material__slug",
        to_field_name="slug",
        queryset=ProductMaterial.objects.all()
    )
    product = filters.ModelMultipleChoiceFilter(
        field_name="product__slug",
        to_field_name="slug",
        queryset=Product.objects.all()
    )
    part = filters.RangeFilter(field_name="part")

    class Meta:
        model = ProductMaterialProduct
        fields = ("material", "product", "part")


class ProductImageFilter(filters.FilterSet):
    product = filters.ModelMultipleChoiceFilter(
        field_name='product__slug',
        to_field_name='slug',
        queryset=Product.objects.all()
    )
    color = filters.ModelMultipleChoiceFilter(
        field_name='product_color__slug',
        to_field_name='slug',
        queryset=ProductColor.objects.all()
    )

    class Meta:
        model = ProductImage
        fields = ('product', 'color')


class ReviewFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name="user__username",
        to_field_name="username",
        queryset=User.objects.all()
    )
    product = filters.ModelMultipleChoiceFilter(
        field_name="product__slug",
        to_field_name="slug",
        queryset=Product.objects.all()
    )

    class Meta:
        model = Review
        fields = ('user', 'product', 'rating')
