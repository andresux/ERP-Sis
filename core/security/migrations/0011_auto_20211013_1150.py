# Generated by Django 2.2.1 on 2021-10-13 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0010_auto_20210923_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessusers',
            name='hostname',
            field=models.TextField(default='inplanet01'),
        ),
        migrations.AlterField(
            model_name='databasebackups',
            name='hostname',
            field=models.TextField(blank=True, default='inplanet01', null=True),
        ),
    ]