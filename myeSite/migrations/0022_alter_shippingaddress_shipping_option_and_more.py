# Generated by Django 5.0.6 on 2024-08-10 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0021_shippingoption_alter_shippingaddress_shipping_option_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_option',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='ShippingOption',
        ),
    ]
