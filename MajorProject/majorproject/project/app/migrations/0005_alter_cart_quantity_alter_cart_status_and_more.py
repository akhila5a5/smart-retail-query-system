# Generated by Django 5.1.3 on 2025-02-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
