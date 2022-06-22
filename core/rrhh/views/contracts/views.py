import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.rrhh.forms import Contracts, ContractsForm
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class ContractsListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Contracts
    template_name = 'contracts/list.html'
    permission_required = 'view_contracts'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('contracts_create')
        context['title'] = 'Listado de Contratos'
        return context


class ContractsCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Contracts
    template_name = 'contracts/create.html'
    form_class = ContractsForm
    success_url = reverse_lazy('contracts_list')
    permission_required = 'add_contracts'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                Contracts.objects.filter(emp_id=request.POST['emp'], state=True).update(state=False)
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Contrato'
        context['action'] = 'add'
        return context


class ContractsUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Contracts
    template_name = 'contracts/create.html'
    form_class = ContractsForm
    success_url = reverse_lazy('contracts_list')
    permission_required = 'change_contracts'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = ContractsForm(instance=self.object, edit=True)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                form = ContractsForm(request.POST, instance=self.get_object(), edit=True)
                data = form.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Contrato'
        context['action'] = 'edit'
        return context


class ContractsDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Contracts
    template_name = 'contracts/delete.html'
    success_url = reverse_lazy('contracts_list')
    permission_required = 'delete_contracts'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Contracts.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
