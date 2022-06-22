import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.college.forms import CommentsForm, Comments
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin

from core.security.models import AccessUsers

class CommentsListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Comments
    template_name = 'comments/student/list.html'
    permission_required = 'view_comments'

    def get_queryset(self):
        return Comments.objects.filter(pers_id=self.request.user.person.id)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('comments_student_create')
        context['title'] = 'Listado de Comentarios y Quejas'
        return context


class CommentsCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Comments
    template_name = 'comments/student/create.html'
    form_class = CommentsForm
    success_url = reverse_lazy('comments_student_list')
    permission_required = 'add_comments'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                comm = Comments()
                comm.pers_id = request.user.person.id
                comm.message = request.POST['message']
                comm.save()
                if self.request.user.is_authenticated:
                    AccessUsers(user_creation=self.request.user, event="Agregar Comentario").save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Comentario o Queja'
        context['action'] = 'add'
        return context


class CommentsUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Comments
    template_name = 'comments/student/create.html'
    form_class = CommentsForm
    success_url = reverse_lazy('comments_student_list')
    permission_required = 'change_comments'

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
                comm = Comments.objects.get(pk=self.get_object().id)
                comm.pers_id = request.user.person.id
                comm.message = request.POST['message']
                comm.save()
                if self.request.user.is_authenticated:
                    AccessUsers(user_creation=self.request.user, event="Editar Comentario").save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Comentario'
        context['action'] = 'edit'
        return context


class CommentsDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Comments
    template_name = 'comments/student/delete.html'
    success_url = reverse_lazy('comments_student_list')
    permission_required = 'delete_comments'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Comments.objects.get(pk=self.get_object().id).delete()
            if self.request.user.is_authenticated:
                AccessUsers(user_creation=self.request.user, event="Borrar Comentario").save()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
