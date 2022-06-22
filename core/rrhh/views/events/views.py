import json

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.rrhh.forms import EventsForm, Events
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class EventsListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Events
    template_name = 'events/list.html'
    permission_required = 'view_events'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('events_create')
        context['title'] = 'Listado de Eventos'
        return context


class EventsCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Events
    template_name = 'events/create.html'
    form_class = EventsForm
    success_url = reverse_lazy('events_list')
    permission_required = 'add_events'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Evento'
        context['action'] = 'add'
        return context


class EventsUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Events
    template_name = 'events/create.html'
    form_class = EventsForm
    success_url = reverse_lazy('events_list')
    permission_required = 'change_events'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Evento'
        context['action'] = 'edit'
        return context


class EventsDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Events
    template_name = 'events/delete.html'
    success_url = reverse_lazy('events_list')
    permission_required = 'delete_events'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Events.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context

