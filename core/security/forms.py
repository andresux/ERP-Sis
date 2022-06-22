from django.forms import *
from .models import *


class ModuleTypeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ModuleType
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'icon': TextInput(attrs={'placeholder': 'ingrese un icono de font awesone'}),
        }
        exclude = ['user_updated', 'user_creation', 'date_updated', 'date_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

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


class ModuleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.pop('instance', None)
        self.fields['type'].widget.attrs['disabled'] = True
        self.fields['type'].required = False
        print(instance)
        if instance is not None:
            self.fields['type'].widget.attrs['disabled'] = not instance.is_vertical
            self.fields['type'].required = instance.is_vertical
        self.fields['url'].widget.attrs['autofocus'] = True

    class Meta:
        model = Module
        fields = '__all__'
        widgets = {
            'url': TextInput(attrs={'placeholder': 'Ingrese url'}),
            'type': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'required': False}),
            'name': TextInput(attrs={'placeholder': 'Ingrese nombre'}),
            'description': TextInput(attrs={'placeholder': 'Ingrese descripción'}),
            'icon': TextInput(attrs={'placeholder': 'ingrese icono de font awesone'}),
            'content_type': Select(
                attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
        }
        exclude = ['user_updated', 'user_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

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


class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = 'name', 'modules'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese nombre'}),
        }
        exclude = []

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    modules = ModelMultipleChoiceField(label='Módulos', queryset=Module.objects.all(), widget=SelectMultiple(
        attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width:100%'}))


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'system_name': TextInput(attrs={'placeholder': 'Ingrese un nombre del sistema'}),
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'icon': TextInput(attrs={'placeholder': 'Ingrese un icono de font awesome'}),
            'layout': Select(attrs={'class': 'form-control select2','style': 'width: 100%'}),
            'navbar': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'brand_logo': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'card': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'sidebar': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'proprietor': TextInput(attrs={'placeholder': 'Ingrese el nombre del propietario'}),
            'ruc': TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'phone': TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'mobile': TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'schedule': TextInput(attrs={'placeholder': 'Ingrese un horario'}),
            'address': TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'mission': Textarea(attrs={'placeholder': 'Ingrese una misión', 'rows': 3, 'cols': 3}),
            'vision': Textarea(attrs={'placeholder': 'Ingrese una visión', 'rows': 3, 'cols': 3}),
            'about_us': Textarea(
                attrs={'placeholder': 'Ingrese una decripción de acerca de nosotros', 'rows': 3, 'cols': 3}),
        }
        exclude = ['user_creation', 'user_updated']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

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


class TemplateForm(forms.Form):
    layout_temp = ChoiceField(choices=layout_options,
                              widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%'}),
                              label='Diseño')
    navbar_temp = ChoiceField(choices=navbar,
                              widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%'}),
                              label='Navbar')
    brand_logo_temp = ChoiceField(choices=brand_logo,
                                  widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%'}),
                                  label='Brand Logo')
    card_temp = ChoiceField(choices=card, widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%'}),
                            label='Card')
    sidebar_temp = ChoiceField(choices=sidebar,
                               widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%'}),
                               label='Sidebar')
