# Generated by Django 5.0.6 on 2024-08-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0024_alter_shippingaddress_shipping_option_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
