from django.forms import *
from core.home.choices import months
from core.ingress.models import *
from core.rrhh.models import Contracts


class ReportForm(forms.Form):
    year = CharField(widget=TextInput(attrs={
        'id': 'year',
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#year',
    }))

    month = ChoiceField(choices=months, widget=Select(
        attrs={
            'id': 'month',
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    date_joined = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'date_joined',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#date_joined'
        }))

    date_range = CharField(widget=TextInput(attrs={'id': 'date_range'}))

    start_date = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={'id': 'start_date', 'value': datetime.now().strftime('%Y-%m-%d')}))

    end_date = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={'id': 'end_date', 'value': datetime.now().strftime('%Y-%m-%d')}))

    contracts = ModelChoiceField(queryset=Contracts.objects.filter(state=True), widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))
