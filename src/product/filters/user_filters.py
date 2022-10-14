from django.db.models import Q
from django_filters import rest_framework as filters

from config.models import GENDER_CHOICES
from user.models import User
from product.models import *


__all__ = (
    'CategoryFilter',
    'ProductFilter',
    'ProductMaterialFilter',
    'ManufacturerFilter',
    'ImageFilter',
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
    gender = filters.ChoiceFilter(choices=GENDER_CHOICES)

    category = filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    manufacturer = filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__slug',
        to_field_name='slug',
        queryset=Manufacturer.objects.all()
    )
    material = filters.ModelMultipleChoiceFilter(
        field_name='materials__slug',
        to_field_name='slug',
        queryset=Material.objects.all()
    )
    color = filters.ModelMultipleChoiceFilter(
        field_name='details__color__slug',
        to_field_name='slug',
        queryset=Color.objects.all()
    )
    size = filters.ModelMultipleChoiceFilter(
        field_name='details__size__name',
        to_field_name='name',
        queryset=Size.objects.all()
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
        fields = ('search', 'price', 'gender', 'manufacturer', 'category', 'material', 'color', 'size')


class ManufacturerFilter(filters.FilterSet):
    country = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Manufacturer
        fields = ('country', )


class ProductMaterialFilter(filters.FilterSet):
    material = filters.ModelMultipleChoiceFilter(
        field_name='material__slug',
        to_field_name='slug',
        queryset=Material.objects.all()
    )
    product = filters.ModelMultipleChoiceFilter(
        field_name='product__slug',
        to_field_name='slug',
        queryset=Product.objects.all()
    )
    part = filters.RangeFilter(field_name='part')

    class Meta:
        model = ProductMaterial
        fields = ('material', 'product', 'part')


class ImageFilter(filters.FilterSet):
    product = filters.ModelMultipleChoiceFilter(
        field_name='product__slug',
        to_field_name='slug',
        queryset=Product.objects.all()
    )
    color = filters.ModelMultipleChoiceFilter(
        field_name='color__slug',
        to_field_name='slug',
        queryset=Color.objects.all()
    )

    class Meta:
        model = Image
        fields = ('product', 'color')


class ReviewFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name='user__username',
        to_field_name='username',
        queryset=User.objects.all()
    )
    product = filters.ModelMultipleChoiceFilter(
        field_name='product__slug',
        to_field_name='slug',
        queryset=Product.objects.all()
    )

    rating = filters.NumberFilter()

    class Meta:
        model = Review
        fields = ('user', 'product', 'rating')
