import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from config.settings import STUDENT, TEACHER
from core.college.forms import PersonForm, Person, User, PersonChangeForm
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class StudentListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Person
    template_name = 'student/list.html'
    permission_required = 'view_person'

    def get_queryset(self):
        return Person.objects.filter(type='estudiante')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('student_create')
        context['title'] = 'Listado de Estudiantes'
        return context


class StudentCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Person
    template_name = 'student/create.html'
    form_class = PersonForm
    success_url = reverse_lazy('student_list')
    permission_required = 'add_person'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PersonForm()
        del form.fields['profession']
        del form.fields['cvitae']
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'username':
                if User.objects.filter(username__iexact=obj):
                    data['valid'] = False
            elif type == 'dni':
                if User.objects.filter(dni=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def validate_type_person(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            data = {'valid': not Person.objects.filter(type=type).exclude(
                type__in=['socio', 'secretaria', 'oficial', 'chofer', 'boletero']).exists()}
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.set_password(user.dni)
                    user.username = user.generate_username()
                    user.email = request.POST['email']
                    user.is_active = True
                    user.save()

                    pers = Person()
                    pers.user = user
                    pers.address = request.POST['address']
                    pers.birthdate = request.POST['birthdate']
                    pers.mobile = request.POST['mobile']
                    pers.conventional = request.POST['conventional']
                    pers.gender = request.POST['gender']
                    pers.type = 'estudiante'
                    pers.save()

                    group = Group.objects.get(pk=STUDENT)
                    user.groups.add(group)
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'validate_type_person':
                return self.validate_type_person()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Estudiante'
        context['action'] = 'add'
        return context


class StudentUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Person
    template_name = 'student/create.html'
    form_class = PersonChangeForm
    success_url = reverse_lazy('student_list')
    permission_required = 'change_person'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PersonChangeForm(instance=self.object.user, initial={
            'id': self.object.id,
            'mobile': self.object.mobile,
            'conventional': self.object.conventional,
            # 'prof': self.object.prof,
            'birthdate': self.object.birthdate,
            'address': self.object.address,
            # 'type': self.object.type,
            'gender': self.object.gender
        })
        del form.fields['profession']
        del form.fields['cviate']
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if type == 'username':
                if User.objects.filter(username__iexact=obj).exclude(person__in=[id]):
                    data['valid'] = False
            elif type == 'dni':
                if User.objects.filter(dni=obj).exclude(person__in=[id]):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email__iexact=obj).exclude(person__in=[id]):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def validate_type_person(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            id = self.get_object().id
            data = {'valid': not Person.objects.filter(type=type).exclude(
                type__in=['socio', 'secretaria', 'oficial', 'chofer', 'boletero']).exclude(id=id).exists()}
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                with transaction.atomic():
                    pers = Person.objects.get(pk=self.get_object().id)
                    pers.address = request.POST['address']
                    pers.birthdate = request.POST['birthdate']
                    pers.mobile = request.POST['mobile']
                    pers.conventional = request.POST['conventional']
                    pers.gender = request.POST['gender']
                    pers.type = 'estudiante'
                    pers.save()

                    user = pers.user
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    elif 'image-clear' in request.POST:
                        user.remove_img()
                        user.image = None
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.email = request.POST['email']
                    user.is_active = True
                    user.save()

                    group = Group.objects.get(pk=STUDENT)
                    user.groups.clear()
                    user.groups.add(group)

            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'validate_type_person':
                return self.validate_type_person()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Estudiante'
        context['action'] = 'edit'
        return context


class StudentDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Person
    template_name = 'student/delete.html'
    success_url = reverse_lazy('student_list')
    permission_required = 'delete_person'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            emp = Person.objects.get(pk=self.get_object().id)
            emp.user.delete()
            emp.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
