# Generated by Django 5.0.6 on 2024-09-24 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0022_productsalesrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsalesrecord',
            name='code',
            field=models.CharField(blank=True, default='361SVT', max_length=8, null=True),
        ),
    ]
