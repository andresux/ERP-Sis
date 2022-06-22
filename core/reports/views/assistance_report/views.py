import json
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from core.reports.forms import ReportForm
from core.rrhh.models import Assistance, Contracts, AssistanceDet
from core.security.mixins import AccessModuleMixin


class AssistanceReportView(AccessModuleMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = ReportForm()
        context['title'] = 'Informe de Asistencias'
        return render(request, 'assistance_report/report.html', context)

    def search_report(self):
        data = []
        try:
            month = self.request.POST.get('month', '')
            year = self.request.POST.get('year', '')
            contract = self.request.POST.get('contract', '')
            search = AssistanceDet.objects.filter()

            if len(year):
                search = search.filter(assist__year=year)
            if len(month):
                search = search.filter(assist__month=month)
            if len(contract):
                search = search.filter(cont_id=contract)

            for i in search:
                data.append([
                    i.assist.year,
                    i.assist.get_month_display(),
                    i.assist.day,
                    i.hour.strftime('%H:%M %p'),
                    i.cont.emp.user.get_full_name(),
                    'Asistio' if i.state else 'Falto',
                ])
        except:
            pass
        return data

    def get_percentage(self, month, valor):
        days = 31
        if month in [1, 3, 5, 7, 8, 10, 12]:
            days = 31
        elif month in [4, 6, 9, 11]:
            days = 30
        elif month in [2]:
            days = 29
        percentage = (valor * 100) / days
        return percentage

    def search_report_teacher(self):
        data = []
        try:
            month = self.request.POST.get('month', '')
            year = self.request.POST.get('year', '')
            contract = self.request.POST.get('contract', '')
            teachers = Contracts.objects.filter(state=True)

            if len(contract):
                teachers = teachers.filter(id=contract)

            for t in teachers:
                assist = t.days_lab(year=year, month=month)
                faults = t.get_faults(year=year, month=month)
                data.append(
                    [
                        t.emp.user.get_full_name(),
                        self.get_percentage(month=month, valor=assist),
                        self.get_percentage(month=month, valor=faults)
                    ]
                )
        except Exception as e:
            print(e)
        return data

    def search_assistance_graph(self):
        data = []
        try:
            month = self.request.POST.get('month', '')
            year = self.request.POST.get('year', '')

            for c in Contracts.objects.filter(state=True):
                data.append({
                    'name': c.emp.user.get_full_name(),
                    'y': c.days_lab(year=year, month=month)
                })
        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        data = {}
        try:
            if action == 'search_report':
                data = self.search_report()
            elif action == 'search_assistance_graph':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.search_assistance_graph(),
                }
            elif action == 'search_report_teacher':
                data = self.search_report_teacher()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')
