import json
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from core.reports.forms import ReportForm
from core.rrhh.models import Contracts
from core.security.mixins import AccessModuleMixin


class ContractsReportView(AccessModuleMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = ReportForm()
        context['title'] = 'Informe de Contratos'
        return render(request, 'contracts_report/report.html', context)

    def search_report(self):
        data = []
        try:
            filter = self.request.POST.get('filter', '')
            month = self.request.POST.get('month', '')
            start_date = self.request.POST.get('start_date', '')
            end_date = self.request.POST.get('end_date', '')
            year = self.request.POST.get('year', '')
            search = Contracts.objects.filter()
            if filter == '1':
                search = search.filter(start_date__range=[start_date, end_date])
            elif filter == '2':
                search = search.filter(start_date__year=year)
            elif filter == '3':
                search = search.filter(start_date__year=year, start_date__month=month)
            for i in search:
                data.append([
                    i.get_nro(),
                    i.emp.user.get_full_name(),
                    i.job.name,
                    i.start_date_format(),
                    i.end_date_format(),
                    i.rmu_format(),
                    'Activo' if i.state else 'Inactivo'
                ])
        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        data = {}
        try:
            if action == 'search_report':
                data = self.search_report()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')