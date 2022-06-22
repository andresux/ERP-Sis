import json

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView

from core.ingress.forms import CtasPay, CtasPayPaymentsForm, CtasPayPayments
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class CtasPayListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = CtasPay
    template_name = 'ctas_pay/list.html'
    permission_required = 'view_ingress'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def check_pays(self, id):
        try:
            cta = CtasPay.objects.get(pk=id)
            pays = CtasPayPayments.objects.filter(cta_id=cta.id).aggregate(resp=Coalesce(Sum('valor'), 0.00))['resp']
            cta.saldo = float(cta.total) - float(pays)
            cta.state = False if cta.saldo <= 0.00 else True
            cta.save()
        except:
            pass

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'load':
                data = []
                for i in CtasPay.objects.filter():
                    data.append(i.toJSON())
            elif action == 'search_pays':
                ctas = CtasPay.objects.get(pk=request.POST['id'])
                data = []
                for i in ctas.ctaspaypayments_set.all():
                    data.append(i.toJSON())
            elif action == 'payment':
                det = CtasPayPayments()
                det.cta_id = request.POST['id']
                det.date_joined = request.POST['date_joined']
                det.valor = float(request.POST['valor'])
                det.details = request.POST['details']
                det.bank_id = request.POST['bank']
                det.account_number = request.POST['account_number']
                det.save()
                self.check_pays(id=det.cta_id)
            elif action == 'delete_pay':
                id = request.POST['id']
                det = CtasPayPayments.objects.get(pk=id)
                cta = det.cta
                det.delete()
                self.check_pays(id=cta.id)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cuentas por Pagar'
        context['form'] = CtasPayPaymentsForm()
        return context


class CtasPayDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = CtasPay
    template_name = 'ctas_pay/delete.html'
    success_url = reverse_lazy('ctas_pay_list')
    permission_required = 'delete_ctaspay'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            CtasPay.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context