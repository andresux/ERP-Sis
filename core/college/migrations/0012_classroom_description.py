# Generated by Django 2.2.1 on 2021-09-10 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0011_auto_20200705_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='description',
            field=models.CharField(default=1, max_length=150, verbose_name='Descripción'),
            preserve_default=False,
        ),
    ]
