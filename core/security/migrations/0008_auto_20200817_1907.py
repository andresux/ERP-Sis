# Generated by Django 2.2.1 on 2020-08-18 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0007_auto_20200817_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessusers',
            name='hostname',
            field=models.TextField(default='DESKTOP-7VNEDK2'),
        ),
        migrations.AlterField(
            model_name='databasebackups',
            name='hostname',
            field=models.TextField(blank=True, default='DESKTOP-7VNEDK2', null=True),
        ),
    ]
