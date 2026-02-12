# Generated migration for shop app - tables match Laravel demo_205 schema intent.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'pay_type',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'product_type',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('C', 'Coming Soon'), ('S', 'On Sale'), ('D', 'Deleted')], default='C', max_length=1)),
                ('name', models.CharField(blank=True, db_index=True, max_length=80, null=True)),
                ('introduction', models.TextField(blank=True)),
                ('photo', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('remain_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_type', models.ForeignKey(db_column='product_type', default=1, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.producttype')),
            ],
            options={
                'db_table': 'products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buy_count', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=18)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pay_type', models.ForeignKey(db_column='pay_type', on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='shop.paytype')),
                ('product', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='shop.product')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'transactions',
                'ordering': ['-created_at', '-id'],
            },
        ),
    ]
