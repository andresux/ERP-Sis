from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from core.college.models import Person
from core.home.choices import type_elementsrol, months, type_event
from core.models import BaseModel


class Job(BaseModel):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['id']


class Contracts(BaseModel):
    emp = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Empleado')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Cargo')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    rmu = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return 'Empleado: {} / Cargo: {} ({} | {}) / Sueldo: ${}'.format(self.emp.user.get_full_name(),
                                                                                    self.job.name,
                                                                                    self.start_date_format(),
                                                                                    self.end_date_format(), self.rmu_format())

    def toJSON(self):
        item = model_to_dict(self)
        item['emp'] = self.emp.toJSON()
        item['job'] = self.job.toJSON()
        item['start_date'] = self.start_date_format()
        item['end_date'] = self.end_date_format()
        item['daysalary'] = format(self.day_salary(), '.2f')
        item['rmu'] = self.rmu_format()
        return item

    def get_nro(self):
        return '%06d' % self.id

    def rmu_format(self):
        return format(self.rmu, '.2f')

    def start_date_format(self):
        return self.start_date.strftime('%Y-%m-%d')

    def end_date_format(self):
        return self.end_date.strftime('%Y-%m-%d')

    def day_salary(self):
        return self.rmu / 24

    def days_lab(self, year, month):
        return self.assistancedet_set.filter(assist__year=year, assist__month=month, state=True).count()

    def get_salary(self, year, month):
        days_lab = self.days_lab(year, month)
        if days_lab > 24:
            return self.rmu
        return days_lab * float(self.day_salary())

    def get_faults(self, year, month):
        return self.assistancedet_set.filter(assist__year=year, assist__month=month, state=False).count()

    def generate_dsctos(self, rmu):
        details = []
        ingress = 0.00
        egress = 0.00
        for element in ElementsRol.objects.all():  # ingreso entra egreso sale
            valor = float(rmu) * float(element.calculation)
            item = element.toJSON()
            item['valor'] = format(valor, '.2f')
            details.append(item)
            if element.type == 1:
                ingress += valor
            elif element.type == 2:
                egress += valor
        total = float(rmu) - ingress + egress
        data = {
            'ingress': format(ingress, '.2f'),
            'egress': format(egress, '.2f'),
            'total': format(total, '.2f'),
            'details': details,
        }
        return data

    def get_state_display(self):
        if self.state:
            return 'Activo'
        return 'Inactivo'

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-id']


class Events(BaseModel):
    cont = models.ForeignKey(Contracts, on_delete=models.CASCADE, verbose_name='Empleado')
    type = models.CharField(max_length=100, choices=type_event, verbose_name='Tipo')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    details = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')

    def __str__(self):
        return self.details

    def toJSON(self):
        item = model_to_dict(self)
        item['cont'] = self.cont.toJSON()
        item['type'] = self.get_type_display()
        item['start_date'] = self.start_date_format()
        item['end_date'] = self.end_date_format()
        return item

    def start_date_format(self):
        return self.start_date.strftime('%Y-%m-%d')

    def end_date_format(self):
        return self.end_date.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-id']


class ElementsRol(BaseModel):
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    type = models.IntegerField(choices=type_elementsrol, verbose_name='Tipo')
    calculation = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Porcentaje')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['type_id'] = self.type
        item['type'] = self.get_type_display()
        item['type_id'] = self.type
        item['calculation'] = self.calculation_format()
        return item

    def calculation_format(self):
        return format(self.calculation, '.2f')

    class Meta:
        verbose_name = 'Elemento del Rol'
        verbose_name_plural = 'Elementos del Rol'
        ordering = ['-id']


class Salary(BaseModel):
    date_joined = models.DateField(default=datetime.now)
    year = models.IntegerField()
    month = models.IntegerField(choices=months, default=1)
    cont = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    dayslab = models.IntegerField(default=0)
    rmu = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    ingress = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    egress = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.cont.emp.user.get_full_name()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined_format()
        item['cont'] = self.cont.toJSON()
        item['ingress'] = self.ingress_format()
        item['rmu'] = self.rmu_format()
        item['egress'] = self.egress_format()
        item['total'] = self.total_format()
        item['month'] = self.get_month_display()
        return item

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def total_format(self):
        return format(self.total, '.2f')

    def rmu_format(self):
        return format(self.rmu, '.2f')

    def ingress_format(self):
        return format(self.ingress, '.2f')

    def egress_format(self):
        return format(self.egress, '.2f')

    def delete(self, using=None, keep_parents=False):
        try:
            self.salarydet_set.all().delete()
        except:
            pass
        super(Salary, self).delete()

    class Meta:
        verbose_name = 'Rol de Pago'
        verbose_name_plural = 'Roles de Pago'
        ordering = ['-id']


class SalaryDet(BaseModel):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    element = models.ForeignKey(ElementsRol, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.element.name

    def valor_format(self):
        return format(self.valor, '.2f')

    def toJSON(self):
        item = model_to_dict(self)
        item['element'] = self.element.toJSON()
        item['valor'] = self.valor_format()
        return item

    class Meta:
        verbose_name = 'Salario Det'
        verbose_name_plural = 'Salarios Det'
        ordering = ['-id']


class Assistance(BaseModel):
    date_joined = models.DateField(default=datetime.now)
    year = models.IntegerField()
    month = models.IntegerField(choices=months, default=1)
    day = models.IntegerField()

    def __str__(self):
        return str(self.day)

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined_format()
        item['month'] = self.get_month_display()
        item['present'] = self.present()
        item['faults'] = self.faults()
        item['assistances'] = [i.toJSON() for i in self.assistancedet_set.all()]
        return item

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def faults(self):
        return self.assistancedet_set.filter(state=False).count()

    def present(self):
        return self.assistancedet_set.filter(state=True).count()

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-id']


class AssistanceDet(BaseModel):
    hour = models.TimeField(default=datetime.now)
    assist = models.ForeignKey(Assistance, on_delete=models.CASCADE)
    cont = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, null=True, blank=True, on_delete=models.SET_NULL)
    desc = models.CharField(max_length=500, null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.cont.emp.user.get_full_name()

    def toJSON(self):
        item = model_to_dict(self, exclude=['assist'])
        item['cont'] = self.cont.toJSON()
        item['hour'] = self.hour.strftime('%H:%M %p')
        if self.event:
            item['event'] = self.event.toJSON()
        return item

    class Meta:
        verbose_name = 'Asistencia Det'
        verbose_name_plural = 'Asistencias Det'
        ordering = ['-id']
