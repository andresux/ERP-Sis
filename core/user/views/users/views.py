import json
from django.db import transaction
from config.settings import HOME
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from core.user.forms import UserForm, ProfileForm
from core.security.models import *
from django.contrib.auth.forms import PasswordChangeForm


class UserListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'reset_password':
                user = User.objects.get(id=request.POST['id'])
                user.set_password(user.dni)
                user.save()
            elif action == 'login_with_user':
                from django.contrib.auth import login
                admin = User.objects.get(pk=request.POST['id'])
                login(request, admin)
            elif action == 'change_password':
                user = User.objects.get(pk=request.POST['id'])
                user.set_password(request.POST['password'])
                user.save()
            elif action == 'search_groups':
                data = User.objects.get(pk=request.POST['id']).get_groups()
            elif action == 'search_access':
                data = User.objects.get(pk=request.POST['id']).get_access_users()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('user_create')
        context['title'] = 'Listado de Administradores'
        return context


class UserCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = User
    template_name = 'user/create.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')
    permission_required = 'add_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return super().get_form()

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni__iexact=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email__iexact=obj):
                    data['valid'] = False
            elif type == 'username':
                if User.objects.filter(username__iexact=obj):
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
        context['title'] = 'Nuevo registro de un Administrador'
        context['action'] = 'add'
        return context


class UserUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = User
    template_name = 'user/create.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')
    permission_required = 'change_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni__iexact=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email__iexact=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'username':
                if User.objects.filter(username__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

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
        context['title'] = 'Edición de un Administrador'
        context['action'] = 'edit'
        return context


class UserDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'delete_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            User.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class UserChangePasswordView(AccessModuleMixin, FormView):
    template_name = 'user/change_pwd.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        request.session['module'] = None
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form = super(UserChangePasswordView, self).get_form_kwargs()
        form['user'] = self.request.user
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'change_pwd':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambio de clave'
        context['action'] = 'change_pwd'
        return context


class UserUpdateProfileView(AccessModuleMixin, UpdateView):
    model = User
    template_name = 'user/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        request.session['module'] = None
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            id = self.request.user.id
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni__iexact=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email__iexact=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'username':
                if User.objects.filter(username__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

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
        context['form'] = ProfileForm(instance=self.request.user)
        context['list_url'] = self.success_url
        context['title'] = 'Edición del perfil'
        context['action'] = 'edit'
        return context


class ChangeProfileView(View):
    def get(self, request, pk):
        try:
            group = Group.objects.filter(id=pk)
            request.session['group'] = None if not group.exists() else group[0]
        except:
            pass
        return HttpResponseRedirect(HOME)
