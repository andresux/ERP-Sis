# Generated by Django 2.2.1 on 2019-12-28 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0003_auto_20191227_0655'),
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
