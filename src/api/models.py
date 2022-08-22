from django.db import models
from config.models import TimeStampMixin, genders_choices


class Category(TimeStampMixin):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    logo = models.CharField(max_length=100, unique=True, verbose_name='Лого')
    parent_category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='Родительская категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['-created_at']


class Product(TimeStampMixin):
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.PROTECT, verbose_name='Производитель')
    gender = models.CharField(max_length=1, choices=genders_choices, verbose_name='Пол')
    is_new = models.BooleanField(default=True, verbose_name='Новинка')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    discount = models.IntegerField(default=0, verbose_name='Скидка %')
    default_color = models.ForeignKey('ProductColor', on_delete=models.PROTECT, verbose_name='Цвет по умолчанию')

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
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Название товара')
    product_color = models.ForeignKey('ProductColor', on_delete=models.PROTECT, verbose_name='Цвет товара')
    product_size = models.ForeignKey('ProductSize', on_delete=models.PROTECT, verbose_name='Размер товара')
    stored = models.IntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = 'Детали товаров'
        verbose_name = 'Детали товара'
        unique_together = ['product', 'product_color', 'product_size']
        ordering = ['-product']
        get_latest_by = '-created_at'


class Manufacturer(TimeStampMixin):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
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


class ProductSize(models.Model):
    size = models.CharField(max_length=3, verbose_name='Размер')  # computed

    def __str__(self):
        return self.size

    class Meta:
        verbose_name_plural = 'Размеры товаров'
        verbose_name = 'Размер товара'
        ordering = ['size']


class ProductColor(models.Model):
    color = models.CharField(max_length=20, unique=True, verbose_name='Название')
    color_hex = models.CharField(max_length=7, verbose_name='Код')  # computed

    def __str__(self):
        return self.color

    class Meta:
        verbose_name_plural = 'Цвета товаров'
        verbose_name = 'Цвет товара'
        ordering = ['color_hex']


class ProductMaterial(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    products = models.ManyToManyField('Product', through='productmaterial_product', verbose_name='Товары')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Материалы продуктов'
        verbose_name = 'Материал продукта'
        ordering = ['name']


class productmaterial_product(models.Model):
    product_material = models.ForeignKey('ProductMaterial', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    part = models.IntegerField(default=100)

    class Meta:
        unique_together = (('product_material', 'product'),)
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_part_between_1_and_100',
                check=models.Q(part__range=(1, 100)),
            ),
        )


class ProductImage(TimeStampMixin):
    product_color = models.ForeignKey('ProductColor', on_delete=models.PROTECT, verbose_name='Цвет')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Фотографии продуктов'
        verbose_name = 'Фотография продукта'
        ordering = ['-product']
        get_latest_by = '-created_at'


class Review(TimeStampMixin):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    rating = models.IntegerField(verbose_name='Оценка')
    text = models.TextField(max_length=1000, verbose_name='Текст')  # computed

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} -> {self.product.title}'

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        unique_together = ['user', 'product']
        ordering = ['-product']
        get_latest_by = '-created_at'
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_rating_between_0_and_10',
                check=models.Q(rating__range=(0, 10)),
            ),
        )


class Coupon(TimeStampMixin):
    is_valid = models.BooleanField(default=False, verbose_name='Активный')  # Coupon isn't active after creating
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=20, unique=True, verbose_name='Название')
    discount = models.IntegerField(verbose_name='Скидка %')
    valid_until = models.DateTimeField(verbose_name='Действителен до')
    use_limit = models.IntegerField(null=True, blank=True, verbose_name='Лимит использований')
    used_amount = models.IntegerField(default=0, verbose_name='Количество использований')
    categories = models.ManyToManyField('Category', verbose_name='Категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Купоны'
        verbose_name = 'Купон'
        ordering = ['-is_valid', '-valid_until']
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
        )


class Order(TimeStampMixin):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    deliverer = models.ForeignKey('Deliverer', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Доставщик')
    point = models.ForeignKey('Point', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Точка')
    delivery_date = models.DateTimeField(default=None, null=True, blank=True, verbose_name='Дата доставки')
    delivery_price = models.IntegerField(default=0, verbose_name='Цена доставки')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering = ['-created_at']
        get_latest_by = '-created_at'
        constraints = (
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_deliverer_and_address_or_point",
                check=(
                        models.Q(deliverer__isnull=False, address__isnull=False, point__isnull=True)
                        | models.Q(deliverer__isnull=True, address__isnull=True, point__isnull=False)
                )
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_delivery_price_greater_then_0_or_equal",
                check=models.Q(delivery_price__gte=0)
            ),
        )


class OrderDetails(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    product_details = models.ForeignKey('ProductDetails', on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name='товар')
    unit_price = models.IntegerField(verbose_name='Цена за штуку')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    discount = models.IntegerField(default=0, verbose_name='Скидка %')

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name_plural = 'Детали заказов'
        verbose_name = 'Детали заказа'
        unique_together = ['order', 'product_details']
        ordering = ['-order']
        get_latest_by = '-created_at'
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_unit_price_greater_then_0',
                check=models.Q(unit_price__gt=0)
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_quantity_greater_then_0',
                check=models.Q(quantity__gt=0)
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_discount_between_0_and_99',
                check=models.Q(discount__range=(0, 99))
            ),
        )


class Deliverer(TimeStampMixin):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')  # computed, max phone length = 15
    delivery_price = models.IntegerField(verbose_name='Цена доставки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Доставщики'
        verbose_name = 'Доставщик'
        ordering = ['delivery_price']
        get_latest_by = '-created_at'


class Point(TimeStampMixin):
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')  # computed, max phone length = 15
    address = models.CharField(max_length=255, verbose_name='Адрес')
    location = models.CharField(max_length=40, verbose_name='Местоположение')  # computed (with one space)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = 'Точки'
        verbose_name = 'Точка'
        ordering = ['-created_at']
        get_latest_by = '-created_at'
