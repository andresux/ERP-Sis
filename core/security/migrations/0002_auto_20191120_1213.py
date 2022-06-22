# Generated by Django 2.2.1 on 2019-11-20 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('security', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduletype',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_moduletype_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='moduletype',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_moduletype_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Tabla'),
        ),
        migrations.AddField(
            model_name='module',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='security.ModuleType', verbose_name='Tipo de Módulo'),
        ),
        migrations.AddField(
            model_name='module',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_module_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_module_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupmodule',
            name='groups',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='groupmodule',
            name='modules',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='security.Module'),
        ),
        migrations.AddField(
            model_name='databasebackups',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_databasebackups_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='databasebackups',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_databasebackups_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_company_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_company_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accessusers',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_accessusers_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accessusers',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_accessusers_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
