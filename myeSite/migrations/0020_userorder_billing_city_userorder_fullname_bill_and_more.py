# Generated by Django 5.0.6 on 2024-09-16 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0019_userorder_shipping_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='billing_city',
            field=models.CharField(default='brt', max_length=100),
        ),
        migrations.AddField(
            model_name='userorder',
            name='fullname_bill',
            field=models.CharField(default='shyam', max_length=100),
        ),
        migrations.AddField(
            model_name='userorder',
            name='fullname_ship',
            field=models.CharField(default='ram', max_length=100),
        ),
    ]
