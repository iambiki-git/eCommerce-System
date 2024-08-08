# Generated by Django 5.0.6 on 2024-07-29 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='new_price',
            field=models.DecimalField(decimal_places=2, default=400, max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=500, max_digits=10, null=True),
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]