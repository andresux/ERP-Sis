import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView

from core.ingress.forms import *
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class IngressListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Ingress
    template_name = 'ingress/list.html'
    permission_required = 'view_ingress'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_details':
                data = []
                for inv in Inventory.objects.filter(ing_id=request.POST['id']):
                    data.append(inv.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('ingress_create')
        context['title'] = 'Listado de Pedidos de Compras'
        return context


class IngressCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Ingress
    template_name = 'ingress/create.html'
    form_class = IngressForm
    success_url = reverse_lazy('ingress_list')
    permission_required = 'add_ingress'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_prov(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Provider.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'ruc':
                if Provider.objects.filter(ruc__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    ingress = Ingress()
                    ingress.prov_id = items['prov']
                    ingress.payment = int(items['payment'])
                    ingress.date_joined = items['date_joined']
                    ingress.save()

                    for p in items['products']:
                        prod = Product.objects.get(pk=p['id'])
                        inv = Inventory()
                        inv.ing = ingress
                        inv.prod_id = prod.id
                        inv.cant = int(p['cant'])
                        inv.saldo = inv.cant
                        inv.price = float(p['cost'])
                        inv.save()

                    ingress.calculate_invoice()

                    if ingress.payment == 2:
                        cta = CtasPay()
                        cta.ing = ingress
                        cta.date_joined = items['date_joined']
                        cta.end_date = items['end_date']
                        cta.total = ingress.total
                        cta.saldo = ingress.total
                        cta.save()
            elif action == 'search_product':
                products = json.loads(request.POST['products'])
                data = []
                for p in Product.objects.filter(name__icontains=request.POST['term']).order_by('name').exclude(
                        id__in=products)[:10]:
                    data.append(p.toJSON())
            elif action == 'search_prov':
                data = []
                for p in Provider.objects.filter(name__icontains=request.POST['term']).order_by('name')[0:10]:
                    data.append(p.toJSON())
            elif action == 'validate_prov':
                return self.validate_prov()
            elif action == 'create_prov':
                c = Provider()
                c.name = request.POST['name']
                c.mobile = request.POST['mobile']
                c.address = request.POST['address']
                c.email = request.POST['email']
                c.ruc = request.POST['ruc']
                c.save()
            elif action == 'validate_serie':
                series = json.loads(request.POST['series'])
                data['resp'] = Inventory.objects.filter(serie=request.POST['code']).exclude(serie__in=series).exists()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['frmProv'] = ProviderForm()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Pedido de Compra'
        context['action'] = 'add'
        return context


class IngressDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Ingress
    template_name = 'ingress/delete.html'
    success_url = reverse_lazy('ingress_list')
    permission_required = 'delete_ingress'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Provider.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
