# Generated by Django 2.2.1 on 2020-07-05 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0009_auto_20191229_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='notes',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='notes',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='notes',
            name='user_updated',
        ),
    ]
