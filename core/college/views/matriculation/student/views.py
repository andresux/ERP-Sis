import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.college.forms import MatriculationForm, Matriculation, Course, TeacherMatterDet
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
from datetime import datetime


class MatriculationListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Matriculation
    template_name = 'matriculation/student/list.html'
    permission_required = 'view_matriculation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Matriculation.objects.filter(student_id=self.request.user.person.id)

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
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('matriculation_student_create')
        context['title'] = 'Listado de Matriculas'
        return context


class MatriculationCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Matriculation
    template_name = 'matriculation/student/create.html'
    form_class = MatriculationForm
    success_url = reverse_lazy('matriculation_student_list')
    permission_required = 'add_matriculation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            course = self.request.POST['course']
            if len(course):
                course = Course.objects.get(pk=course)
                yearnow = datetime.now().date().year
                if Matriculation.objects.filter(student_id=self.request.user.person.id, date_joined__year=yearnow):
                    data = {'valid': False, 'message': 'El estudiante ya cuenta con una matricula para este año lectivo'}
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                matr = Matriculation()
                matr.student_id = request.user.person.id
                matr.course_id = int(request.POST['course'])
                matr.save()
            elif action == 'search_matters':
                data = []
                id = request.POST['id']
                if len(id):
                    course = Course.objects.get(pk=id)
                    for i in course.coursemat_set.all():
                        item = i.mat.toJSON()
                        teacher = i.teachermatterdet_set.all()
                        if teacher:
                            item['teacher'] = teacher[0].teacher_mat.teacher.user.get_full_name()
                        else:
                            item['teacher'] = 'Sin asignar'
                        data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Matricula'
        context['action'] = 'add'
        return context


class MatriculationUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Matriculation
    template_name = 'matriculation/student/create.html'
    form_class = MatriculationForm
    success_url = reverse_lazy('matriculation_student_list')
    permission_required = 'change_matriculation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Matriculation.objects.filter(name__iexact=obj).exclude(pk=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Matricula'
        context['action'] = 'edit'
        return context


class MatriculationDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Matriculation
    template_name = 'matriculation/student/delete.html'
    success_url = reverse_lazy('matriculation_student_list')
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
