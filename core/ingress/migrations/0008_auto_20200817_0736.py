# Generated by Django 2.2.1 on 2020-08-17 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0007_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='cost',
        ),
    ]