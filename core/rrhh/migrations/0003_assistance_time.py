# Generated by Django 2.2.1 on 2020-08-18 00:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0002_auto_20191230_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistance',
            name='time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]
