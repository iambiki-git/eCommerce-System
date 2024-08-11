# Generated by Django 5.0.6 on 2024-08-09 09:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0014_shippingoption_alter_shippingaddress_shipping_option'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_option',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='OrderTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=255)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qty', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('billing_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myeSite.billingaddress')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='myeSite.product')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myeSite.shippingaddress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ShippingOption',
        ),
    ]
