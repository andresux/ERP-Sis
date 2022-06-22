import json

from django.contrib.admin.models import LogEntry
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView

from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
from core.security.models import *


class AuditListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = LogEntry
    template_name = 'audit/list.html'
    permission_required = 'view_logentry'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'delete_all':
                LogEntry.objects.all().delete()
            elif action == 'search':
                data = []
                date_joined = datetime.strptime(request.POST.get("date_joined", datetime.now()), '%Y-%m-%d')
                for i in LogEntry.objects.filter(action_time__year=date_joined.year,
                                                 action_time__month=date_joined.month,
                                                 action_time__day=date_joined.day):
                    data.append({
                        'id': i.id,
                        'date_joined': i.action_time.strftime('%Y-%m-%d'),
                        'hour': i.action_time.strftime('%H:%M %p'),
                        'module': i.object_repr,
                        'action': i.change_message,
                        'username': i.user.username,
                    })
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Logs de Seguridad'
        return context


class AuditDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = LogEntry
    template_name = 'audit/delete.html'
    success_url = reverse_lazy('audit_list')
    permission_required = 'delete_logentry'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            LogEntry.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
