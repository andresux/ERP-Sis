# Generated by Django 2.2.1 on 2021-10-21 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0025_typecourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='type_course',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='college.TypeCourse'),
            preserve_default=False,
        ),
    ]
