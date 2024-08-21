# Generated by Django 5.0.6 on 2024-08-21 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0006_userorder_billing_add_userorder_shipping_add'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='billing_add',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myeSite.billingaddress'),
        ),
        migrations.AlterField(
            model_name='userorder',
            name='shipping_add',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myeSite.shippingaddress'),
        ),
    ]
