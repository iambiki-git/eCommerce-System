# Generated by Django 5.0.6 on 2024-09-25 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0028_remove_productsalesrecord_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Received', 'Received'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
