# Generated by Django 2.2.1 on 2021-10-21 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0026_course_type_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='type_course',
        ),
    ]