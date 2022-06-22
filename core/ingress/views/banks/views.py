import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.ingress.forms import BanksForm
from core.ingress.models import *
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class BanksListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Banks
    template_name = 'banks/list.html'
    permission_required = 'view_banks'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('banks_create')
        context['title'] = 'Listado de Bancos'
        return context


class BanksCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Banks
    template_name = 'banks/create.html'
    form_class = BanksForm
    success_url = reverse_lazy('banks_list')
    permission_required = 'add_banks'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Banks.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'ruc':
                if Banks.objects.filter(ruc=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Banco'
        context['action'] = 'add'
        return context


class BanksUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Banks
    template_name = 'banks/create.html'
    form_class = BanksForm
    success_url = reverse_lazy('banks_list')
    permission_required = 'change_banks'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'name':
                if Banks.objects.filter(name__iexact=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'ruc':
                if Banks.objects.filter(ruc=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Banco'
        context['action'] = 'edit'
        return context


class BanksDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Banks
    template_name = 'banks/delete.html'
    success_url = reverse_lazy('banks_list')
    permission_required = 'delete_banks'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Banks.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
