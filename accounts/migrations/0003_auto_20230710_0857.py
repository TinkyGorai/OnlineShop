# Generated by Django 3.2.19 on 2023-07-10 03:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_cart_cartitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coupon_code', models.CharField(max_length=50)),
                ('is_expired', models.BooleanField(default=True)),
                ('discount_amount', models.IntegerField(blank=True)),
                ('minimum_amount', models.IntegerField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='accounts.cart'),
        ),
    ]
