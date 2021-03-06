import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.security.forms import ModuleTypeForm
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
from core.security.models import *


class ModuleTypeListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = ModuleType
    template_name = 'module_type/list.html'
    permission_required = 'view_moduletype'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('module_type_create')
        context['title'] = 'Listado de Tipos de Módulos'
        return context


class ModuleTypeCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = ModuleType
    template_name = 'module_type/create.html'
    form_class = ModuleTypeForm
    success_url = reverse_lazy('module_type_list')
    permission_required = 'add_moduletype'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if ModuleType.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'icon':
                if ModuleType.objects.filter(icon__iexact=obj):
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
        context['title'] = 'Nuevo registro de un Tipo de Módulo'
        context['action'] = 'add'
        return context


class ModuleTypeUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = ModuleType
    template_name = 'module_type/create.html'
    form_class = ModuleTypeForm
    success_url = reverse_lazy('module_type_list')
    permission_required = 'change_moduletype'

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
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if ModuleType.objects.filter(name__iexact=obj).exclude(pk=id):
                    data['valid'] = False
            elif type == 'icon':
                if ModuleType.objects.filter(icon__iexact=obj).exclude(pk=id):
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
        context['title'] = 'Edición de un Tipo de Módulo'
        context['action'] = 'edit'
        return context


class ModuleTypeDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = ModuleType
    template_name = 'module_type/delete.html'
    success_url = reverse_lazy('module_type_list')
    permission_required = 'delete_moduletype'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            ModuleType.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
