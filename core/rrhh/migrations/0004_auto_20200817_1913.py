# Generated by Django 2.2.1 on 2020-08-18 00:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0003_assistance_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assistance',
            name='time',
        ),
        migrations.AddField(
            model_name='assistancedet',
            name='time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]
