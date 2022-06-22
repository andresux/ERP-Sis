import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.college.forms import *
from core.college.models import Person
from core.security.mixins import AccessModuleMixin


class StudentCourseAdminListView(AccessModuleMixin, FormView):
    form_class = StudentCourseForm
    template_name = 'student_course/admin_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_teacher':
                data = []
                course = request.POST['id']
                for i in Person.objects.filter(teachermatter__teachermatterdet__course_mat__course_id=course).exclude(type='estudiante').distinct():
                    item = i.toJSON()
                    item['text'] = i.user.get_full_name()
                    data.append(item)
            elif action == 'search_matter':
                data = []
                course = request.POST['course']
                teacher = request.POST['teacher']
                for i in TeacherMatterDet.objects.filter(course_mat__course_id=course, teacher_mat__teacher_id=teacher):
                    item = i.toJSON()
                    item['text'] = i.course_mat.mat.name
                    data.append(item)
            elif action == 'search_students':
                data = []
                course = request.POST['course']
                id = request.POST['id']
                print(id)
                print(course)
                for d in Matriculation.objects.filter(course_id=course, course__coursemat__teachermatterdet__id=id):
                    data.append(d.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Estudiantes por Curso/Docente'
        return context


class StudentCourseTeacherListView(AccessModuleMixin, FormView):
    form_class = StudentCourseForm
    template_name = 'student_course/teacher_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        teacher_ids = TeacherMatterDet.objects.filter(teacher_mat__teacher_id=self.request.user.person.id).values_list('id', flat=True)
        form = StudentCourseForm()
        form.fields['course'].queryset = Course.objects.filter(coursemat__teachermatterdet__in=teacher_ids).distinct()
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_matter':
                data = []
                course = request.POST['course']
                for i in TeacherMatterDet.objects.filter(course_mat__course_id=course, teacher_mat__teacher_id=request.user.person.id):
                    item = i.toJSON()
                    item['text'] = i.course_mat.mat.name
                    data.append(item)
            elif action == 'search_students':
                data = []
                course = request.POST['course']
                id = request.POST['id']
                for d in Matriculation.objects.filter(course_id=course, course__coursemat__teachermatterdet__id=id):
                    data.append(d.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Estudiantes por Curso y Docente'
        return context
