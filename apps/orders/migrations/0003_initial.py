# Generated by Django 4.1.2 on 2023-02-04 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('orders', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.address', verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='deliverer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.deliverer', verbose_name='Доставщик'),
        ),
        migrations.AddField(
            model_name='order',
            name='point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.point', verbose_name='Точка'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('unit_price__gt', 0)), name='orders_orderdetails_unit_price_greater_then_0'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gt', 0)), name='orders_orderdetails_quantity_greater_then_0'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('discount__range', (0, 99))), name='orders_orderdetails_discount_between_0_and_99'),
        ),
        migrations.AlterUniqueTogether(
            name='orderdetails',
            unique_together={('order', 'product_details')},
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('address__isnull', False), ('deliverer__isnull', False), ('point__isnull', True)), models.Q(('address__isnull', True), ('deliverer__isnull', True), ('point__isnull', False)), _connector='OR'), name='orders_order_deliverer_and_address_or_point'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(check=models.Q(('delivery_price__gte', 0)), name='orders_order_delivery_price_greater_then_0_or_equal'),
        ),
    ]
