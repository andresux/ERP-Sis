import json
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.college.forms import TeacherMatterForm, TeacherMatter, TeacherMatterDet, CourseMat
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class TeacherMatterListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = TeacherMatter
    template_name = 'teacher_matter/list.html'
    permission_required = 'view_teachermatter'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_matters':
                data = []
                teacher = TeacherMatter.objects.get(pk=request.POST['id'])
                for item in teacher.teachermatterdet_set.all():
                    data.append(item.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('teacher_matter_create')
        context['title'] = 'Listado de Materias o Módulos por Docente'
        return context


class TeacherMatterCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = TeacherMatter
    template_name = 'teacher_matter/create.html'
    form_class = TeacherMatterForm
    success_url = reverse_lazy('teacher_matter_list')
    permission_required = 'add_teachermatter'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            teacher = self.request.POST['teacher']
            period = self.request.POST['period']
            if len(teacher) and len(period):
                if TeacherMatter.objects.filter(teacher_id=teacher, period_id=period):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    tmat = TeacherMatter()
                    tmat.teacher_id = int(items['teacher'])
                    tmat.period_id = int(items['period'])
                    tmat.save()
                    for mat in items['matters']:
                        det = TeacherMatterDet()
                        det.teacher_mat_id = tmat.id
                        det.course_mat_id = mat['id']
                        det.save()
            elif action == 'search_matters':
                data = []
                ids = json.loads(request.POST['ids'])
                period = int(request.POST['period'])
                for i in CourseMat.objects.filter(course__period_id=period).exclude(id__in=ids):
                    item = i.toJSON()
                    if not TeacherMatterDet.objects.filter(course_mat_id=i.id).exists():
                        item['state'] = TeacherMatterDet.objects.filter(course_mat_id=i.id).exists()
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
        context['title'] = 'Nuevo registro de las materias o módulos de un docente'
        context['action'] = 'add'
        context['matters'] = []
        return context


class TeacherMatterUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = TeacherMatter
    template_name = 'teacher_matter/create.html'
    form_class = TeacherMatterForm
    success_url = reverse_lazy('teacher_matter_list')
    permission_required = 'change_teachermatter'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = TeacherMatterForm(instance=self.get_object(), edit=True)
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            teacher = self.request.POST['teacher']
            period = self.request.POST['period']
            if len(teacher) and len(period):
                if TeacherMatter.objects.filter(teacher_id=teacher, period_id=period).exclude(id=self.get_object().id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    tmat = TeacherMatter.objects.get(pk=self.get_object().id)
                    tmat.teacher_id = int(items['teacher'])
                    tmat.period_id = int(items['period'])
                    tmat.save()
                    tmat.teachermatterdet_set.all().delete()
                    for mat in items['matters']:
                        det = TeacherMatterDet()
                        det.teacher_mat_id = tmat.id
                        det.course_mat_id = mat['id']
                        det.save()
            elif action == 'search_matters':
                data = []
                ids = json.loads(request.POST['ids'])
                period = int(request.POST['period'])
                for i in CourseMat.objects.filter(course__period_id=period).exclude(id__in=ids):
                    item = i.toJSON()
                    item['state'] = False
                    data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_matters(self):
        data = []
        try:
            teach_mat = TeacherMatter.objects.get(pk=self.get_object().id)
            for i in teach_mat.teachermatterdet_set.all():
                data.append(i.course_mat.toJSON())
        except:
            pass
        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Periodo'
        context['action'] = 'edit'
        context['matters'] = self.get_matters()
        return context


class TeacherMatterDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = TeacherMatter
    template_name = 'period/delete.html'
    success_url = reverse_lazy('period_list')
    permission_required = 'delete_period'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            TeacherMatter.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
