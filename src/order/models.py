from math import ceil

from django.db import models

from config.models import TimeStampMixin
from product.models import ProductDetails
from user.models import *

__all__ = (
    'Order',
    'OrderDetails',
    'Deliverer',
    'Point',
)


class Order(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    point = models.ForeignKey('Point', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Точка')
    deliverer = models.ForeignKey(
        'Deliverer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Доставщик'
    )
    user_address = models.ForeignKey(
        UserAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Адрес доставки'
    )

    @property
    def total_price(self):
        price = 0
        for order_detail in self.order_details.all():
            price += order_detail.unit_price * order_detail.quantity * (1 - order_detail.discount / 100)
        return ceil(price)

    total_price.fget.short_description = 'Сумма заказа'

    delivery_date = models.DateTimeField(default=None, null=True, blank=True, verbose_name='Дата доставки')
    delivery_price = models.IntegerField(default=0, verbose_name='Цена доставки')
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
                        models.Q(deliverer__isnull=False, user_address__isnull=False, point__isnull=True)
                        | models.Q(deliverer__isnull=True, user_address__isnull=True, point__isnull=False)
                )
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_delivery_price_greater_then_0_or_equal",
                check=models.Q(delivery_price__gte=0)
            ),
        )


class OrderDetails(models.Model):
    order = models.ForeignKey('Order', related_name='order_details', on_delete=models.CASCADE, verbose_name='Заказ')
    product_details = models.ForeignKey(
        ProductDetails,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='товар'
    )

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
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')  # the length is fitted
    delivery_price = models.IntegerField(verbose_name='Цена доставки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Доставщики'
        verbose_name = 'Доставщик'
        ordering = ['delivery_price']
        get_latest_by = '-created_at'


class Point(TimeStampMixin):
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')  # the length is fitted
    address = models.CharField(max_length=255, verbose_name='Адрес')
    location = models.CharField(max_length=22, verbose_name='Местоположение')  # the length is fitted (without spaces)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = 'Точки'
        verbose_name = 'Точка'
        ordering = ['-created_at']
        get_latest_by = '-created_at'
