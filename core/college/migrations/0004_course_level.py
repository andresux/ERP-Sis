# Generated by Django 2.2.1 on 2019-12-29 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0003_auto_20191228_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.IntegerField(choices=[(1, 'Primer grado de educación general básica'), (2, 'Segundo grado de educación general básica'), (3, 'Tercer grado de educación general básica'), (4, 'Cuarto grado de educación general básica'), (5, 'Quinto grado de educación general básica'), (6, 'Sexto grado de educación general básica'), (7, 'Séptimo grado de educación general básica'), (8, 'Octavo grado de educación general básica'), (9, 'Noveno grado de educación general básica'), (10, 'Décimo grado de educación general básica')], default=1),
        ),
    ]
