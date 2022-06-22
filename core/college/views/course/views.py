import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.college.forms import CourseForm, Course, Matter, CourseMat
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class CourseListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Course
    template_name = 'course/list.html'
    permission_required = 'view_course'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_matters':
                data = []
                course = Course.objects.get(pk=request.POST['id'])
                for i in course.coursemat_set.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('course_create')
        context['title'] = 'Listado de Cursos'
        return context


class CourseCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Course
    template_name = 'course/create.html'
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    permission_required = 'add_course'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            classroom = self.request.POST['classroom'].strip()
            period = self.request.POST['period']
            level = self.request.POST['level']
            if len(period) and len(classroom) and len(level):
                if Course.objects.filter(period_id=period, level=level, classroom_id=classroom):
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
                    course = Course()
                    course.period_id = int(items['period'])
                    course.classroom_id = int(items['classroom'])
                    course.level = int(items['level'])
                    course.save()
                    for p in items['matters']:
                        det = CourseMat()
                        det.course_id = course.id
                        det.mat_id = int(p['id'])
                        det.save()
            elif action == 'search_mat':
                ids = json.loads(request.POST['ids'])
                data = []
                for p in Matter.objects.filter(name__icontains=request.POST['term']).order_by('name').exclude(id__in=ids)[:10]:
                    item = p.toJSON()
                    item['value'] = p.name
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
        context['title'] = 'Nuevo registro de un Curso'
        context['action'] = 'add'
        context['matters'] = []
        return context


class CourseUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Course
    template_name = 'course/create.html'
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    permission_required = 'change_course'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

    def validate_data(self):
        data = {'valid': True}
        try:
            classroom = self.request.POST['classroom']
            period = self.request.POST['period']
            level = self.request.POST['level']
            if len(period) and len(classroom) and len(level):
                if Course.objects.filter(period_id=period, level=level, classroom_id=classroom).exclude(id=self.get_object().id):
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
                    course = Course.objects.get(pk=self.get_object().id)
                    course.period_id = int(items['period'])
                    course.classroom_id = int(items['classroom'])
                    course.level = int(items['level'])
                    course.save()
                    course.coursemat_set.all().delete()
                    for p in items['matters']:
                        det = CourseMat()
                        det.course_id = course.id
                        det.mat_id = int(p['id'])
                        det.save()
            elif action == 'search_mat':
                ids = json.loads(request.POST['ids'])
                data = []
                for p in Matter.objects.filter(name__icontains=request.POST['term']).order_by('name').exclude(
                        id__in=ids)[:10]:
                    item = p.toJSON()
                    item['value'] = p.name
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
            course = Course.objects.get(pk=self.get_object().id)
            for i in course.coursemat_set.all():
                data.append(i.mat.toJSON())
        except:
            pass
        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Curso'
        context['action'] = 'edit'
        context['matters'] = self.get_matters()
        return context


class CourseDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Course
    template_name = 'course/delete.html'
    success_url = reverse_lazy('course_list')
    permission_required = 'delete_course'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Course.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
