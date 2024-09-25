# Generated by Django 5.0.6 on 2024-09-25 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0025_alter_product_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Received', 'Received'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
