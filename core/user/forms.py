from django.forms import *
from .models import User


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].required = True
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Ingrese sus nombres'}),
            'last_name': TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}),
            'username': TextInput(attrs={'placeholder': 'Ingrese un username'}),
            'dni': TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
            'groups': SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width:100%'}),
        }
        exclude = ['is_change_password', 'is_active', 'is_staff', 'user_permissions', 'password', 'date_joined', 'last_login', 'is_superuser']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    token = CharField(widget=HiddenInput(), required=False)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Ingrese sus nombres'}),
            'last_name': TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}),
            'username': TextInput(attrs={'placeholder': 'Ingrese un username'}),
            'dni': TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
        }
        exclude = ['is_change_password', 'is_active', 'is_staff', 'user_permissions', 'password', 'date_joined', 'last_login', 'is_superuser', 'groups']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    token = CharField(widget=HiddenInput(), required=False)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data