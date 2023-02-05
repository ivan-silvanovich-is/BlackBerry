from django.db.models import Q
from django_filters import rest_framework as filters

from apps.core.filters import *
from apps.users.models import User
from .user_filters import *
from ..models import *

__all__ = (
    'StaffCategoryFilter',
    'StaffProductFilter',
    'StaffProductDetailsFilter',
    'StaffManufacturerFilter',
    'StaffMaterialFilter',
    'StaffProductMaterialFilter',
    'StaffColorFilter',
    'StaffSizeFilter',
    'StaffImageFilter',
    'StaffReviewFilter',
    'StaffCouponFilter',
)


class StaffCategoryFilter(CategoryFilter, TimeStampFilter):
    name = filters.CharFilter(lookup_expr='contains')
    logo = filters.CharFilter(lookup_expr='contains')

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('parent_category', 'parent_category'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'parent_category': 'Родительская категория',
        }
    )

    class Meta:
        model = Category
        fields = ('created_at', 'updated_at', 'parent_category', 'child_categories', 'name', 'logo', 'order',)


class StaffProductFilter(ProductFilter, TimeStampFilter):
    default_color = filters.ModelMultipleChoiceFilter(
        field_name='default_color__slug',
        to_field_name='slug',
        queryset=Color.objects.all()
    )

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('price', 'price'),
            ('is_new', 'new'),
            ('discount', 'discount'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'price': 'Цена',
            'is_new': 'Новизна',
            'discount': 'Скидка',
        }
    )

    class Meta:
        model = Product
        fields = (
            'search', 'created_at', 'updated_at', 'price', 'gender', 'manufacturer', 'category', 'material', 'color',
            'default_color', 'size', 'order',
        )


class StaffProductDetailsFilter(TimeStampFilter, DateOrderFilter):
    product = filters.ModelMultipleChoiceFilter(
        field_name="product__slug",
        to_field_name="slug",
        queryset=Product.objects.all()
    )
    color = filters.ModelMultipleChoiceFilter(
        field_name="color__slug",
        to_field_name="slug",
        queryset=Color.objects.all()
    )
    size = filters.ModelMultipleChoiceFilter(
        field_name="size__name",
        to_field_name="name",
        queryset=Size.objects.all()
    )

    quantity = filters.RangeFilter()

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('size', 'size'),
            ('color__hex', 'color'),
            ('quantity', 'quantity'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'size': 'Размер',
            'color__hex': 'Цвет',
            'quantity': 'Количество',
        }
    )

    class Meta:
        model = ProductDetails
        fields = ('created_at', 'updated_at', 'product', 'color', 'size', 'quantity', 'order')


class StaffManufacturerFilter(ManufacturerFilter, TimeStampFilter, DateOrderFilter):
    logo = filters.CharFilter(lookup_expr='contains')
    address = filters.CharFilter(lookup_expr='contains')

    search = filters.CharFilter(method='get_found_manufacturers', label='Поиск')

    def get_found_manufacturers(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('country', 'country'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'country': 'Страна',
        },
    )

    class Meta:
        model = Manufacturer
        fields = ('search', 'created_at', 'updated_at', 'logo', 'country', 'address', 'order')


class StaffMaterialFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Material
        fields = ('name',)


class StaffProductMaterialFilter(ProductMaterialFilter):
    order = filters.OrderingFilter(
        fields=(
            ('product', 'product'),
            ('material', 'material'),
        ),
        field_labels={
            'product': 'Продукт',
            'material': 'Материал',
        },
    )

    class Meta:
        model = ProductMaterial
        fields = ('material', 'product', 'part', 'order')


class StaffColorFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    hex_min = filters.CharFilter(field_name='hex', lookup_expr='gte')
    hex_max = filters.CharFilter(field_name='hex', lookup_expr='lte')

    order = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('hex', 'hex'),
        ),
        field_labels={
            'name': 'Название',
            'hex': 'Код',
        },
    )

    class Meta:
        model = Color
        fields = ('name', 'hex_min', 'hex_max', 'order')


class StaffSizeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    order = filters.OrderingFilter(fields=(('name', 'name'), ), field_labels={'name': 'Название', },)

    class Meta:
        model = Size
        fields = ('name', 'order')


class StaffImageFilter(ImageFilter, TimeStampFilter, DateOrderFilter):
    name = filters.CharFilter(lookup_expr='contains')

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('product', 'product'),
            ('color', 'color'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'product': 'Продукт',
            'color': 'Цвет',
        },
    )

    class Meta:
        model = Image
        fields = ('name', 'created_at', 'updated_at', 'product', 'color', 'order')


class StaffReviewFilter(ReviewFilter, TimeStampFilter):
    text = filters.CharFilter(lookup_expr='contains')

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('username', 'username'),
            ('product', 'product'),
            ('rating', 'rating'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'username': 'Имя пользователя',
            'product': 'Продукт',
            'rating': 'Оценка',
        }
    )

    class Meta:
        model = Review
        fields = ('created_at', 'updated_at', 'user', 'product', 'rating', 'text', 'order')


class StaffCouponFilter(TimeStampFilter):
    name = filters.CharFilter(lookup_expr='contains')
    is_active = filters.BooleanFilter()
    discount = filters.RangeFilter()
    valid_until = filters.DateFromToRangeFilter()
    use_limit = filters.RangeFilter()
    used_amount = filters.RangeFilter()

    user = filters.ModelChoiceFilter(
        field_name='user__username',
        to_field_name='username',
        queryset=User.objects.all(),
    )
    category = filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all(),
        label='Категории',
    )

    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('is_active', 'is_active'),
            ('user', 'user'),
            ('discount', 'discount'),
            ('valid_until', 'valid_until'),
            ('use_limit', 'used_limit'),
            ('used_amount', 'used_amount'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
            'is_active': 'Активность купона',
            'user': 'Имя пользователя',
            'discount': 'Скидка',
            'valid_until': 'Дата истечения',
            'use_limit': 'Лимит использований',
            'used_amount': 'Количество использований',
        }
    )

    class Meta:
        model = Coupon
        fields = (
            'created_at', 'updated_at', 'name', 'is_active', 'user', 'discount', 'category', 'valid_until',
            'use_limit', 'used_amount',
        )
