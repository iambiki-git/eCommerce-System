# Generated by Django 5.0.6 on 2024-09-25 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0027_productsalesrecord_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsalesrecord',
            name='status',
        ),
    ]