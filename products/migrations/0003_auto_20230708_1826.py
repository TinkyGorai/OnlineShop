# Generated by Django 3.2.19 on 2023-07-08 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20230708_1754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ColorVariant',
            new_name='color_variant',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='SizeVariant',
            new_name='size_variant',
        ),
    ]
