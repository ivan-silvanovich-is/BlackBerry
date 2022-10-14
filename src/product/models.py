from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config.models import TimeStampMixin, GENDER_CHOICES
from user.models import User

__all__ = (
    'Category',
    'Product',
    'ProductDetails',
    'Material',
    'ProductMaterial',
    'Size',
    'Color',
    'Image',
    'Manufacturer',
    'Review',
    'Coupon',
)


# TODO: add automatic database triggers


class Category(TimeStampMixin):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    logo = models.CharField(max_length=100, unique=True, verbose_name='Лого')

    parent_category = models.ForeignKey(
        'Category',
        related_name='child_categories',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Родительская категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['-created_at']


class Product(TimeStampMixin):
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.PROTECT, verbose_name='Производитель')
    default_color = models.ForeignKey('Color', on_delete=models.PROTECT, verbose_name='Цвет по умолчанию')

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    is_new = models.BooleanField(default=True, verbose_name='Новинка')
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    discount = models.IntegerField(
        default=0,
        verbose_name='Скидка %',
        validators=(MinValueValidator(0), MaxValueValidator(99))
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-created_at']
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_discount_between_0_and_99',
                check=models.Q(discount__range=(0, 99)),
            ),
        )


class ProductDetails(TimeStampMixin):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name='Название товара',
        related_name='details'
    )
    color = models.ForeignKey('Color', on_delete=models.PROTECT, verbose_name='Цвет товара')
    size = models.ForeignKey('Size', on_delete=models.PROTECT, verbose_name='Размер товара')

    quantity = models.IntegerField(default=0, verbose_name='Количество', validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.product.title} {self.color.slug} {self.size.name}'

    class Meta:
        verbose_name_plural = 'Детали товаров'
        verbose_name = 'Детали товара'
        unique_together = ['product', 'color', 'size']
        ordering = ['-product']
        get_latest_by = '-created_at'
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_quantity_greater_then_0_or_equal',
                check=models.Q(quantity__gte=0),
            ),
        )


class Manufacturer(TimeStampMixin):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    logo = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='Логотип')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Описание')
    country = models.CharField(max_length=50, verbose_name='Страна')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Производители'
        verbose_name = 'Производитель'
        ordering = ['name']
        get_latest_by = '-created_at'


class Size(models.Model):
    name = models.CharField(max_length=3, unique=True, verbose_name='Размер')  # the length is fitted

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Размеры товаров'
        verbose_name = 'Размер товара'
        ordering = ['name']


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    hex = models.CharField(max_length=7, unique=True, verbose_name='Код')  # the length is fitted

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Цвета товаров'
        verbose_name = 'Цвет товара'
        ordering = ['hex']


class Material(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    products = models.ManyToManyField(
        'Product',
        through='ProductMaterial',
        related_name='materials',
        through_fields=('material', 'product'),
        verbose_name='Товары'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Материалы товаров'
        verbose_name = 'Материал товара'
        ordering = ['name']


class ProductMaterial(models.Model):  # adjacent table for many-to-many relationship (Material, Product)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    material = models.ForeignKey('Material', on_delete=models.PROTECT, verbose_name='Материал')

    part = models.IntegerField(
        default=100,
        verbose_name='Содержание %',
        validators=(MinValueValidator(0), MaxValueValidator(100)),
    )

    class Meta:
        unique_together = (('material', 'product'),)
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_part_between_1_and_100',
                check=models.Q(part__range=(1, 100)),
            ),
        )


class Image(TimeStampMixin):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='images',
        verbose_name='товар',
    )
    color = models.ForeignKey('Color', on_delete=models.PROTECT, verbose_name='Цвет')

    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Фотографии товаров'
        verbose_name = 'Фотография товара'
        ordering = ['-product', 'color']
        get_latest_by = '-created_at'


class Review(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')

    rating = models.IntegerField(verbose_name='Оценка', validators=(MinValueValidator(0), MaxValueValidator(10)), )
    text = models.TextField(max_length=1000, verbose_name='Текст')  # the length is fitted

    def __str__(self):
        return f'{self.user.full_name} -> {self.product.title}'

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        unique_together = (('user', 'product'),)
        ordering = ['-product', '-created_at']
        get_latest_by = '-created_at'
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_rating_between_0_and_10',
                check=models.Q(rating__range=(0, 10)),
            ),
        )


class Coupon(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')

    is_active = models.BooleanField(default=False, verbose_name='Активный')  # Coupon isn't active after creating
    name = models.CharField(max_length=20, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    discount = models.IntegerField(verbose_name='Скидка %', validators=(MinValueValidator(0), MaxValueValidator(99)),)
    valid_until = models.DateTimeField(verbose_name='Дата истечения')
    use_limit = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Лимит использований',
        validators=(MinValueValidator(1),),
    )
    used_amount = models.IntegerField(
        default=0,
        verbose_name='Количество использований',
        validators=(MinValueValidator(0),),
    )

    categories = models.ManyToManyField('Category', verbose_name='Категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Купоны'
        verbose_name = 'Купон'
        ordering = ['-is_active', '-valid_until']
        get_latest_by = '-created_at'
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_discount_between_0_and_99',
                check=models.Q(discount__range=(0, 99))
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_use_limit_is_null_or_greater_then_0',
                check=(models.Q(use_limit__isnull=True) | models.Q(use_limit__gt=0))
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_used_amount_greater_then_0_or_equal',
                check=models.Q(used_amount__gte=0)
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_used_amount_less_then_use_limit_or_equal',
                check=(models.Q(use_limit__isnull=True) | models.Q(use_limit__gte=models.F('used_amount')))
            ),
        )
