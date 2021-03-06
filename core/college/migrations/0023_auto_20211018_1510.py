# Generated by Django 2.2.1 on 2021-10-18 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0022_auto_20211013_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='archive',
        ),
        migrations.RemoveField(
            model_name='person',
            name='cpay',
        ),
        migrations.AddField(
            model_name='classroom',
            name='minimum_participants',
            field=models.IntegerField(default=1, verbose_name='Minimo de participantes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classroom',
            name='plancurso',
            field=models.FileField(blank=True, null=True, upload_to='plancurso/%Y/%m/%d', verbose_name='Plan de Curso'),
        ),
        migrations.AddField(
            model_name='matter',
            name='silabus',
            field=models.FileField(blank=True, null=True, upload_to='silabus/%Y/%m/%d', verbose_name='silabo de materia'),
        ),
    ]
