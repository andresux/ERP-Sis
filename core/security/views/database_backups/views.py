import json
import subprocess
from django.core.files import File
from django.db import connection
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView
from config.settings import BASE_DIR
from core.security.decorators.module.decorators import get_group_session
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
from core.security.models import *


class DatabaseBackupsListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = DatabaseBackups
    template_name = 'database_backups/list.html'
    permission_required = 'view_databasebackups'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create_backup_sqlite(self):
        db_name = connection.settings_dict['NAME']
        data_now = '{0:%Y-%m-%d_%H:%M:%S}'.format(datetime.now())
        name_backup = "{}_{}.db".format('backup', data_now)
        script = ' {} {} ".backup {}"'.format('sqlite3', db_name, "'{}'".format(name_backup))
        subprocess.call(script, shell=True)
        file = os.path.join(BASE_DIR, name_backup)
        db = DatabaseBackups()
        db.user_creation = self.request.user
        db.archive.save(name_backup, File(open(file, 'rb')), save=False)
        db.save()
        os.remove(file)

    def create_backup_postgresql(self):
        db_name = connection.settings_dict['NAME']
        data_now = '{0:%Y-%m-%d_%H:%M:%S}'.format(datetime.now())
        name_backup = "{}_{}.backup".format('backup', data_now)
        script = 'pg_dump -h localhost -p 5432 -U postgres -F c -b -v -f "{}" {}'.format(name_backup, db_name)
        subprocess.call(script, shell=True)
        file = os.path.join(BASE_DIR, name_backup)
        db = DatabaseBackups()
        db.user_creation = self.request.user
        db.archive.save(name_backup, File(open(file, 'rb')), save=False)
        db.save()
        os.remove(file)

    def verify_permission(self):
        group_id = get_group_session(self.request)
        return Group.objects.get(pk=group_id).permissions.filter(codename='add_databasebackups').exists()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'delete_access_all':
                for d in DatabaseBackups.objects.all():
                    d.delete()
            elif action == 'create':
                if self.verify_permission():
                    db_type = connection.vendor
                    if db_type == 'sqlite':
                        self.create_backup_sqlite()
                    elif db_type == 'postgresql':
                        self.create_backup_postgresql()
                else:
                    data['error'] = 'No tiene permisos para utilizar esta opción'
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de respaldos de la base de datos'
        context['create_url'] = reverse_lazy('database_backups_create')
        return context


class DatabaseBackupsDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = DatabaseBackups
    template_name = 'database_backups/delete.html'
    success_url = reverse_lazy('database_backups_list')
    permission_required = 'delete_databasebackups'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            DatabaseBackups.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
