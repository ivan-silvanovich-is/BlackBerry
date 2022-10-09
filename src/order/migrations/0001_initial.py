# Generated by Django 4.1 on 2022-10-09 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('order', '0001_initial'), ('order', '0002_initial'), ('order', '0003_initial')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliverer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='Телефон')),
                ('delivery_price', models.IntegerField(verbose_name='Цена доставки')),
            ],
            options={
                'verbose_name': 'Доставщик',
                'verbose_name_plural': 'Доставщики',
                'ordering': ['delivery_price'],
                'get_latest_by': '-created_at',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('delivery_date', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата доставки')),
                ('delivery_price', models.IntegerField(default=0, verbose_name='Цена доставки')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Отправлено')),
                ('deliverer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.deliverer', verbose_name='Доставщик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created_at'],
                'get_latest_by': '-created_at',
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='Телефон')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('location', models.CharField(max_length=22, verbose_name='Местоположение')),
            ],
            options={
                'verbose_name': 'Точка',
                'verbose_name_plural': 'Точки',
                'ordering': ['-created_at'],
                'get_latest_by': '-created_at',
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.IntegerField(verbose_name='Цена за штуку')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('discount', models.IntegerField(default=0, verbose_name='Скидка %')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='order.order', verbose_name='Заказ')),
                ('product_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productdetails', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'Детали заказа',
                'verbose_name_plural': 'Детали заказов',
                'ordering': ['-order'],
                'get_latest_by': '-created_at',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.point', verbose_name='Точка'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.useraddress', verbose_name='Адрес доставки'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('unit_price__gt', 0)), name='order_orderdetails_unit_price_greater_then_0'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gt', 0)), name='order_orderdetails_quantity_greater_then_0'),
        ),
        migrations.AddConstraint(
            model_name='orderdetails',
            constraint=models.CheckConstraint(check=models.Q(('discount__range', (0, 99))), name='order_orderdetails_discount_between_0_and_99'),
        ),
        migrations.AlterUniqueTogether(
            name='orderdetails',
            unique_together={('order', 'product_details')},
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('deliverer__isnull', False), ('point__isnull', True), ('user_address__isnull', False)), models.Q(('deliverer__isnull', True), ('point__isnull', False), ('user_address__isnull', True)), _connector='OR'), name='order_order_deliverer_and_address_or_point'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(check=models.Q(('delivery_price__gte', 0)), name='order_order_delivery_price_greater_then_0_or_equal'),
        ),
    ]
