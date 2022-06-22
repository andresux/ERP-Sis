import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView

from core.college.forms import Comments
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class CommentsListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Comments
    template_name = 'comments/admin/list.html'
    permission_required = 'view_comments'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Comentarios y Quejas'
        return context


class CommentsDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Comments
    template_name = 'comments/admin/delete.html'
    success_url = reverse_lazy('comments_admin_list')
    permission_required = 'delete_comments'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Comments.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
