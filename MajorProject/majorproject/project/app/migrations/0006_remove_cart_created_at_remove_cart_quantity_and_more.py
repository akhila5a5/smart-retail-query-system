# Generated by Django 5.1.3 on 2025-02-04 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_cart_quantity_alter_cart_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='status',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardholdername', models.CharField(max_length=100)),
                ('cardnumber', models.IntegerField()),
                ('expirationdate', models.CharField(max_length=100)),
                ('cvv', models.IntegerField()),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usermodel')),
            ],
            options={
                'db_table': 'Orders',
            },
        ),
    ]
