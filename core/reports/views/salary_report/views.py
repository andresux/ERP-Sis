import json
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from core.reports.forms import ReportForm
from core.rrhh.models import Salary
from core.security.mixins import AccessModuleMixin


class SalaryReportView(AccessModuleMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = ReportForm()
        context['title'] = 'Informe de Salarios'
        return render(request, 'salary_report/report.html', context)

    def search_report(self):
        data = []
        try:
            month = self.request.POST.get('month', '')
            year = self.request.POST.get('year', '')
            contract = self.request.POST.get('contract', '')
            search = Salary.objects.filter()

            if len(contract):
               search = search.filter(cont_id=contract)
            if len(year):
                search = search.filter(year=year)
            if len(month):
                search = search.filter(month=month)

            for i in search:
                data.append([
                    i.cont.emp.user.get_full_name(),
                    i.cont.job.name,
                    i.cont.rmu_format(),
                    i.dayslab,
                    format(i.cont.day_salary(), '.2f'),
                    i.rmu_format(),
                    i.ingress_format(),
                    i.egress_format(),
                    i.total_format()
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