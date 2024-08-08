# Generated by Django 5.0.6 on 2024-08-01 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0013_billingaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('charge', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myeSite.shippingoption'),
        ),
    ]