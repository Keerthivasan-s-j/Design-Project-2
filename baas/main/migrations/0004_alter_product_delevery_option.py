# Generated by Django 5.1.2 on 2025-04-25 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_battery_capacity_product_range_per_charge_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='delevery_option',
            field=models.CharField(choices=[('free', 'Free Delevery'), ('paid', 'Paid Delevery')], max_length=10, verbose_name='Delevery Option'),
        ),
    ]
