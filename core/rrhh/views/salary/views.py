import json
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView
from core.rrhh.forms import SalaryForm, Salary, SalaryDet, Contracts, ElementsRol
from core.reports.forms import ReportForm
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class SalaryListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Salary
    template_name = 'salary/list.html'
    permission_required = 'view_salary'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_rolpay':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                for i in Salary.objects.filter(year=year, month=month):
                    item = i.toJSON()
                    data.append(item)
            elif action == 'search_dsctos':
                data = []
                for i in SalaryDet.objects.filter(salary_id=request.POST['id'], element__type=request.POST['type']):
                    data.append(i.toJSON())
                print(data)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('salary_create')
        context['title'] = 'Listado de Salarios'
        context['form'] = ReportForm()
        return context


class SalaryCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Salary
    template_name = 'salary/create.html'
    form_class = SalaryForm
    success_url = reverse_lazy('salary_list')
    permission_required = 'add_salary'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def found_rolpay(self, month, year):
        return Salary.objects.filter(month=month, year=year).exists()

    def validate_data(self):
        data = {'valid': True}
        try:
            year = self.request.POST['year']
            month = self.request.POST['month']
            if len(year) and len(month):
                if Salary.objects.filter(month=month, year=year).exists():
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'create':
                with transaction.atomic():
                    year = request.POST['year']
                    month = request.POST['month']
                    for i in Contracts.objects.filter(state=True):
                        rol = Salary()
                        rol.year = year
                        rol.month = month
                        rol.cont_id = i.id
                        rol.rmu = float(i.get_salary(year, month))
                        rol.dayslab = i.days_lab(year, month)
                        rol.save()

                        for element in ElementsRol.objects.filter():
                            det = SalaryDet()
                            det.salary_id = rol.id
                            det.element_id = element.id
                            det.valor = float(element.calculation) * float(rol.rmu)
                            det.save()
                            if element.type == 1:
                                rol.ingress += det.valor
                            elif element.type == 2:
                                rol.egress += det.valor
                        rol.total = float(rol.rmu) - float(rol.ingress) + float(rol.egress)
                        rol.save()
            elif action == 'generate':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                if len(month) and len(year):
                    if not self.found_rolpay(month, year):
                        for cont in Contracts.objects.filter(state=True):
                            rmu = cont.get_salary(year, month)
                            item = cont.generate_dsctos(rmu)
                            item['cont'] = cont.toJSON()
                            item['daysalary'] = format(cont.day_salary(), '.2f')
                            item['dias_lab'] = cont.days_lab(year, month)
                            item['salary_dayslab'] = format(rmu, '.2f')
                            data.append(item)
                        print(data)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Salario'
        context['action'] = 'add'
        return context


class SalaryDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Salary
    template_name = 'salary/delete.html'
    success_url = reverse_lazy('salary_list')
    permission_required = 'delete_salary'

    def get_object(self, queryset=None):
        return None

    def get(self, request, *args, **kwargs):
        if 'year' in self.kwargs and 'month' in self.kwargs:
            if Salary.objects.filter(year=self.kwargs['year'], month=self.kwargs['month']):
                return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Salary.objects.filter(year=self.kwargs['year'], month=self.kwargs['month']).delete()
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def salary_exits(self, year, month):
        return Salary.objects.filter(year=year, month=month).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
