from django.db.models import Q
from django_filters import rest_framework as filters

from config.models import GENDER_CHOICES
from user.models import User
from .models import *


__all__ = (
    'CategoryFilter',
    'ProductFilter',
    'StaffProductFilter',
    'ProductMaterialFilter',
    'ManufacturerFilter',
    'ProductImageFilter',
    'ReviewFilter',
)


class TimeStampFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    class Meta:
        fields = ('created_at', 'updated_at')


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

    search = filters.CharFilter(method='get_found_products', label='Поиск')

    def get_found_products(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

    order = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('created_at', 'date'),
            ('is_new', 'new'),
            ('discount', 'discount'),
            # ('reviews', 'reviews'),  # TODO: add option to filter by reviews (by count, by average mark)
        ),
        field_labels={
            'price': 'Цена',
            'created_at': 'Дата',
            'is_new': 'Новизна',
            'discount': 'Скидка',
        }
    )

    class Meta:
        model = Product
        fields = ('search', 'price', 'manufacturer', 'category', 'gender', 'material', 'color', 'size')


class StaffProductFilter(ProductFilter, TimeStampFilter):
    pass


class ManufacturerFilter(filters.FilterSet):
    country = filters.AllValuesMultipleFilter(field_name="country", label="Страна")

    class Meta:
        model = Manufacturer
        fields = ('country', )


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
