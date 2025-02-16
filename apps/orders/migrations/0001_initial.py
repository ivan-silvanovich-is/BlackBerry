# Generated by Django 4.1.2 on 2023-02-04 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='orders.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Детали заказа',
                'verbose_name_plural': 'Детали заказов',
                'ordering': ['-order'],
                'get_latest_by': '-created_at',
            },
        ),
    ]
