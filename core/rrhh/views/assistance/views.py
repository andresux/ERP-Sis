import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from core.rrhh.forms import Assistance, AssistanceForm, AssistanceDet, Contracts, Events
from core.reports.forms import ReportForm
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class AssistanceListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Assistance
    template_name = 'assistance/list.html'
    permission_required = 'view_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'load':
                data = []
                items = Assistance.objects.filter(year=request.POST['year'])
                month = request.POST['month']
                if len(month):
                    items = items.filter(month=month)
                data = [i.toJSON() for i in items.order_by('day')]
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('assistance_create')
        context['title'] = 'Listado de Asistencias'
        context['form'] = ReportForm()
        return context


class AssistanceCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assistance_list')
    permission_required = 'add_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def generate_assistance(self):
        data = []
        try:
            date_now = datetime.now().date()
            for i in Contracts.objects.filter(state=True):
                item = i.toJSON()
                item['desc'] = ''
                item['state'] = 0
                events = Events.objects.filter(cont_id=i.id).filter(Q(start_date=date_now) | Q(end_date=date_now))
                if events:
                    item['state'] = 1
                    item['event'] = events[0].toJSON()
                data.append(item)
        except:
            pass
        return data

    def validate_data(self):
        data = {'valid': True}
        try:
            obj = self.request.POST['obj'].strip()
            data['valid'] = True
            if Assistance.objects.filter(date_joined=obj):
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
                    date_joined = datetime.strptime(items['date_joined'], '%Y-%m-%d')
                    a = Assistance()
                    a.date_joined = date_joined
                    a.year = date_joined.year
                    a.month = date_joined.month
                    a.day = date_joined.day
                    a.save()
                    for i in items['assistances']:
                        det = AssistanceDet()
                        det.assist_id = a.id
                        det.cont_id = int(i['id'])
                        det.desc = i['desc']
                        if 'event' in i:
                            det.event_id = int(i['event']['id'])
                            det.state = True
                        else:
                            det.state = i['state']
                        det.save()
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'generate_assistance':
                data = self.generate_assistance()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Asistencia'
        context['action'] = 'add'
        return context


class AssistanceUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assistance_list')
    permission_required = 'change_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = AssistanceForm(instance=self.object, initial={'id': self.object.id}, date_joined_enabled=False)
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if Assistance.objects.filter(date_joined=obj).exclude(id=id):
                data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def generate_assistance(self):
        data = []
        try:
            date_joined = self.request.POST['date_joined']
            for i in Contracts.objects.filter(state=True).order_by('id'):
                item = i.toJSON()
                item['desc'] = ''
                item['state'] = 0
                det = AssistanceDet.objects.filter(cont_id=i.id, assist__date_joined=date_joined)
                if det.exists():
                    assist = det[0]
                    item['desc'] = assist.desc
                    item['state'] = 1 if assist.state else 0
                    if assist.event is not None:
                        item['event'] = assist.event.toJSON()
                        item['state'] = 1
                data.append(item)
        except:
            pass
        print(data)
        return data

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'edit':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    date_joined = datetime.strptime(items['date_joined'], '%Y-%m-%d')
                    a = Assistance.objects.get(pk=self.get_object().id)
                    a.assistancedet_set.all().delete()
                    a.date_joined = date_joined
                    a.year = date_joined.year
                    a.month = date_joined.month
                    a.day = date_joined.day
                    a.save()
                    for i in items['assistances']:
                        det = AssistanceDet()
                        det.assist = a
                        det.cont_id = int(i['id'])
                        det.desc = i['desc']
                        if 'event' in i:
                            det.event_id = int(i['event']['id'])
                            det.state = True
                        else:
                            det.state = i['state']
                        det.save()
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'generate_assistance':
                data = self.generate_assistance()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Asistencia'
        context['action'] = 'edit'
        return context


class AssistanceDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Assistance
    template_name = 'assistance/delete.html'
    success_url = reverse_lazy('assistance_list')
    permission_required = 'delete_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Assistance.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class InsertAssistanceView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            year = datetime.now().year
            month = datetime.now().month
            day = datetime.now().day
            assist = Assistance.objects.filter(year=year, month=month, day=day)
            if assist.exists():
                assist = assist[0]
            else:
                assist = Assistance(year=year, month=month, day=day)
                assist.save()

            contract = self.request.user.person.contracts_set.all()
            if contract.exists():
                contract = contract[0]
                if not AssistanceDet.objects.filter(cont_id=contract, assist_id=assist.id).exists():
                    det = AssistanceDet()
                    det.cont_id = contract.id
                    det.assist_id = assist.id
                    det.state = True
                    det.save()
                else:
                    data = {'error': 'El docente ya se le tomo la asistencia el dia de hoy {}'.format(
                        datetime.now().strftime('%d-%m-%Y'))}
            else:
                data = {'error': 'El usuario no tiene contrato, por lo tanto no se le puede tomar la asistencia'}
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')
