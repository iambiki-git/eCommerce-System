# Generated by Django 5.0.6 on 2024-07-19 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myeSite', '0003_items_category_items_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='desc',
            field=models.TextField(default='This is description.'),
        ),
    ]
