# Generated by Django 5.0.6 on 2024-07-29 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0004_wishlist_added_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
