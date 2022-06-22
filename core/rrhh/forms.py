from .models import *
from django.forms import *


class JobForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
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


class ElementsRolForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ElementsRol
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'type': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'calculation': TextInput()
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


class ContractsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit', False)
        super().__init__(*args, **kwargs)
        self.fields['emp'].widget.attrs['autofocus'] = True
        self.fields['emp'].queryset = Person.objects.filter(type='docente')
        if edit:
            del self.fields['emp']

    class Meta:
        model = Contracts
        widgets = {
            'emp': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'start_date': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
            'job': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'rmu': TextInput()
        }
        exclude = ['state', 'user_updated', 'user_creation']

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


class SalaryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cont'].widget.attrs['autofocus'] = True
        self.fields['cont'].queryset = Contracts.objects.filter(state=True).order_by('id')

    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {
            'year': TextInput(attrs={
                'id': 'year',
                'class': 'form-control datetimepicker-input',
                'data-toggle': 'datetimepicker',
                'data-target': '#year',
            }),
            'month': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class AssistanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        date_joined_enabled = kwargs.pop('date_joined_enabled', True)
        super().__init__(*args, **kwargs)
        if not date_joined_enabled:
            self.fields['date_joined'].widget.attrs['disabled'] = True

    class Meta:
        model = Assistance
        fields = '__all__'
        widgets = {
            'date_joined': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class EventsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        cont_enabled = kwargs.pop('cont_enabled', True)
        super().__init__(*args, **kwargs)
        self.fields['cont'].widget.attrs['autofocus'] = True
        self.fields['cont'].queryset = Contracts.objects.filter(state=True).order_by('id')
        if not cont_enabled:
            del self.fields['cont']

    class Meta:
        model = Events
        fields = '__all__'
        widgets = {
            'cont': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'type': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
            'details': Textarea(attrs={'rows': 3, 'cols': 3, 'placeholder': 'Ingrese una descripción'}),
            'start_date': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
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
