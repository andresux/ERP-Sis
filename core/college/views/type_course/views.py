import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.college.forms import TypeCourseForm, TypeCourse
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class TypeCourseListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = TypeCourse
    template_name = 'type_course/list.html'
    permission_required = 'view_typecourse'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('type_course_create')
        context['title'] = 'Listado de Categorías de Curso'
        return context


class TypeCourseCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = TypeCourse
    template_name = 'type_course/create.html'
    form_class = TypeCourseForm
    success_url = reverse_lazy('type_course_list')
    permission_required = 'add_typecourse'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if TypeCourse.objects.filter(name__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
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
        context['title'] = 'Nuevo registro de una Categoría de Cursos'
        context['action'] = 'add'
        return context


class TypeCourseUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = TypeCourse
    template_name = 'type_course/create.html'
    form_class = TypeCourseForm
    success_url = reverse_lazy('type_course_list')
    permission_required = 'change_typecourse'

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
                if TypeCourse.objects.filter(name__iexact=obj).exclude(pk=id):
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
        context['title'] = 'Edición de un Categoría de Cursos'
        context['action'] = 'edit'
        return context


class TypeCourseDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = TypeCourse
    template_name = 'type_course/delete.html'
    success_url = reverse_lazy('type_course_list')
    permission_required = 'delete_typecourse'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            TypeCourse.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
