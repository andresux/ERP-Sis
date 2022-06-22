import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.college.forms import Unit, UnitForm
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class UnitListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Unit
    template_name = 'unit/list.html'
    permission_required = 'view_unit'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('unit_create')
        context['title'] = 'Listado de unidades'
        return context

class UnitListMatterView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Unit
    template_name = 'unit/list.html'
    permission_required = 'view_unit'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Unit.objects.filter(matter = self.kwargs["pk"]).order_by("number")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('unit_create')
        context['title'] = 'Listado de unidades por materia'
        return context



class UnitCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Unit
    template_name = 'unit/create.html'
    form_class = UnitForm
    success_url = reverse_lazy('unit_list')
    permission_required = 'add_unit'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Unit.objects.filter(name__iexact=obj):
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
        context['title'] = 'Nueva unidad'
        context['action'] = 'add'
        context['add_new_url'] = 'add'
        
        return context


class UnitUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Unit
    template_name = 'unit/create.html'
    form_class = UnitForm
    success_url = reverse_lazy('unit_list')
    permission_required = 'change_unit'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

    def validate_data(self):
        data = {'valid': True}
        try:
            obj = self.request.POST['obj'].strip()
            if self.request.POST['type'] == 'name'and Unit.objects.filter(name__iexact=obj).exclude(pk=self.get_object().id):
                data['valid'] = False
        except Exception as e:
            print(str(e))
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
        context['title'] = 'Edición de una unidad'
        context['action'] = 'edit'
        context['add_new_url'] = 'add'
        return context


class UnitDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Unit
    template_name = 'unit/delete.html'
    success_url = reverse_lazy('unit_list')
    permission_required = 'delete_unit'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Unit.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación de unidad'
        context['list_url'] = self.success_url
        return context
