# Generated by Django 2.2.1 on 2021-10-21 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0028_classroom_type_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='type_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='college.TypeCourse', verbose_name='Tipo de Curso'),
        ),
    ]