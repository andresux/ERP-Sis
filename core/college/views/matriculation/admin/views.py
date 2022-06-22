import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.college.forms import MatrStateForm, Matriculation, Course, TeacherMatterDet
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
from datetime import datetime


class MatriculationListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Matriculation
    template_name = 'matriculation/admin/list.html'
    permission_required = 'view_matriculation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_matters':
                data = []
                matr = Matriculation.objects.get(pk=request.POST['id'])
                for i in matr.course.coursemat_set.all():
                    item = i.mat.toJSON()
                    teacher = i.teachermatterdet_set.all()
                    if teacher:
                        item['teacher'] = teacher[0].teacher_mat.teacher.user.get_full_name()
                    else:
                        item['teacher'] = 'Sin asignar'
                    data.append(item)
            elif action == 'edit_statemat':
                mat = Matriculation.objects.get(pk=request.POST['id'])
                mat.state = request.POST['state']
                mat.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Matriculas de los Estudiantes'
        context['form'] = MatrStateForm()
        return context


class MatriculationDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Matriculation
    template_name = 'matriculation/admin/delete.html'
    success_url = reverse_lazy('matriculation_admin_list')
    permission_required = 'delete_matriculation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Matriculation.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
