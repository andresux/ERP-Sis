# Generated by Django 2.2.1 on 2021-09-23 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0018_remove_person_conventional'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='conventional',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono Convencional'),
        ),
        migrations.AlterField(
            model_name='person',
            name='prof',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='college.Profession', verbose_name='Rol'),
        ),
    ]