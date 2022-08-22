# Generated by Django 4.1 on 2022-08-22 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='productmaterialproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='productmaterialproduct',
            name='product_material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productmaterial', verbose_name='Материал'),
        ),
        migrations.AddField(
            model_name='productmaterial',
            name='products',
            field=models.ManyToManyField(through='api.ProductMaterialProduct', to='api.product', verbose_name='Товары'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product', verbose_name='товар'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productcolor', verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product', verbose_name='Название товара'),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='product_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productcolor', verbose_name='Цвет товара'),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='product_size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productsize', verbose_name='Размер товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='default_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.productcolor', verbose_name='Цвет по умолчанию'),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='product_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.productdetails', verbose_name='товар'),
        ),
        migrations.AddField(
            model_name='order',
            name='deliverer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.deliverer', verbose_name='Доставщик'),
        ),
        migrations.AddField(
            model_name='order',
            name='point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.point', verbose_name='Точка'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='categories',
            field=models.ManyToManyField(to='api.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.category', verbose_name='Родительская категория'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('rating__range', (0, 10))), name='api_review_rating_between_0_and_10'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'product')},
        ),
        migrations.AddConstraint(
            model_name='productmaterialproduct',
            constraint=models.CheckConstraint(check=models.Q(('part__range', (1, 100))), name='api_productmaterialproduct_part_between_1_and_100'),
        ),
        migrations.AlterUniqueTogether(
            name='productmaterialproduct',
            unique_together={('product_material', 'product')},
        ),
        migrations.AlterUniqueTogether(
            name='productdetails',
            unique_together={('product', 'product_color', 'product_size')},
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(('discount__range', (0, 99))), name='api_product_discount_between_0_and_99'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('unit_price__gt', 0)), name='api_orderdetails_unit_price_greater_then_0'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gt', 0)), name='api_orderdetails_quantity_greater_then_0'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('discount__range', (0, 99))), name='api_orderdetails_discount_between_0_and_99'),
        ),
        migrations.AlterUniqueTogether(
            name='orderdetails',
            unique_together={('order', 'product_details')},
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('address__isnull', False), ('deliverer__isnull', False), ('point__isnull', True)), models.Q(('address__isnull', True), ('deliverer__isnull', True), ('point__isnull', False)), _connector='OR'), name='api_order_deliverer_and_address_or_point'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(check=models.Q(('delivery_price__gte', 0)), name='api_order_delivery_price_greater_then_0_or_equal'),
        ),
        migrations.AddConstraint(
            model_name='coupon',
            constraint=models.CheckConstraint(check=models.Q(('discount__range', (0, 99))), name='api_coupon_discount_between_0_and_99'),
        ),
        migrations.AddConstraint(
            model_name='coupon',
            constraint=models.CheckConstraint(check=models.Q(('use_limit__isnull', True), ('use_limit__gt', 0), _connector='OR'), name='api_coupon_use_limit_is_null_or_greater_then_0'),
        ),
        migrations.AddConstraint(
            model_name='coupon',
            constraint=models.CheckConstraint(check=models.Q(('used_amount__gte', 0)), name='api_coupon_used_amount_greater_then_0_or_equal'),
        ),
    ]
