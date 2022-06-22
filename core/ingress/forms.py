from django.forms import *
from .models import *


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

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


class ProviderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese un email'})
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

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


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'cost': TextInput(),
            'cat': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
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


class IngressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prov'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ingress
        fields = '__all__'
        widgets = {
            'prov': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'payment': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'type_payment': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'date_joined': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'subtotal': TextInput(),
            'iva': TextInput(),
            'dscto': TextInput(),
            'total': TextInput()
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class CtasPayPaymentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor'].widget.attrs['autofocus'] = True

    class Meta:
        model = CtasPayPayments
        fields = 'date_joined', 'bank', 'account_number', 'valor', 'details'
        widgets = {
            'date_joined': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'bank': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'account_number': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un número de cuenta'}),
            'valor': TextInput(),
            'details': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una descripción',
                'rows': 3,
                'cols': 3,
                'autocomplete': 'off'
            })
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class InventoryForm(Form):
    product = ModelChoiceField(queryset=Product.objects.filter().order_by('-id'), widget=Select(
        attrs={'id': 'product', 'class': 'form-control select2', 'style': 'width: 100%'}))

    date_joined = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'date_joined',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#date_joined'
        }))


class BanksForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Banks
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

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
