import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from core.ingress.forms import InventoryForm
from core.ingress.models import Inventory
from core.security.mixins import AccessModuleMixin


class InventoryListView(AccessModuleMixin, ListView):
    model = Inventory
    template_name = 'inventory/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search':
                data = []
                date_joined = request.POST.get('date_joined', None)
                product_id = request.POST.get('product', None)
                invs = Inventory.objects.filter()
                if product_id is not None:
                    invs = invs.filter(prod_id=product_id)
                if date_joined is not None and date_joined:
                    invs = invs.filter(ing__date_joined=date_joined)
                for i in invs:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Entrada y Salida de Materiales'
        context['form'] = InventoryForm()
        return context