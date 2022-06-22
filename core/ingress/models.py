from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import model_to_dict
from config.settings import STATIC_URL, MEDIA_URL
from core.college.models import Person
from core.home.choices import type_payment
from datetime import datetime
from core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']


class Product(BaseModel):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria')
    image = models.ImageField(upload_to='plants/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio Unitario')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/default/empty.png')

    def get_stock(self):
        return int(self.inventory_set.filter(saldo__gt=0).aggregate(total=Coalesce(Sum('saldo'), 0)).get('total'))

    def toJSON(self):
        item = model_to_dict(self)
        item['cost'] = format(self.cost, '.2f')
        item['image'] = self.get_image()
        item['cat'] = self.cat.toJSON()
        item['stock'] = self.get_stock()
        item['value'] = self.name
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-name']


class Provider(BaseModel):
    date_joined = models.DateField(default=datetime.now)
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, unique=True, verbose_name='Ruc')
    mobile = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfnoo celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=500, null=True, blank=True, verbose_name='Email')

    def __str__(self):
        return self.name

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined_format()
        item['value'] = self.name
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']


class Ingress(BaseModel):
    prov = models.ForeignKey(Provider, on_delete=models.CASCADE)
    payment = models.IntegerField(choices=type_payment, default=1)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.prov.name

    def toJSON(self):
        item = model_to_dict(self)
        item['nro'] = self.get_nro()
        item['prov'] = self.prov.toJSON()
        item['date_joined'] = self.date_joined_format()
        item['subtotal'] = self.subtotal_format()
        item['dscto'] = self.dscto_format()
        item['iva'] = self.iva_format()
        item['total'] = self.total_format()
        return item

    def get_nro(self):
        return format(self.id, '06d')

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def subtotal_format(self):
        return format(self.subtotal, '.2f')

    def iva_format(self):
        return format(self.iva, '.2f')

    def dscto_format(self):
        return format(self.dscto, '.2f')

    def total_format(self):
        return format(self.total, '.2f')

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.inventory_set.all():
            subtotal += float(d.price) * int(d.cant)
        self.subtotal = subtotal
        self.iva = 0.00
        self.total = float(self.subtotal) - float(self.dscto)
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.inventory_set.all():
                i.delete()
        except:
            pass
        super(Ingress, self).delete()

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-id']


class Inventory(BaseModel):
    ing = models.ForeignKey(Ingress, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.prod.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total = (float(self.price) * self.cant) - float(self.dscto)
        super(Inventory, self).save()

    def toJSON(self):
        item = model_to_dict(self, exclude=['dscto'])
        item['prod'] = self.prod.toJSON()
        item['ing'] = self.ing.toJSON()
        item['price'] = self.price_format()
        item['dscto'] = self.dscto_format()
        item['total'] = self.total_format()
        return item

    def get_nro(self):
        return format(self.id, '06d')

    def total_format(self):
        return format(self.total, '.2f')

    def price_format(self):
        return format(self.price, '.2f')

    def dscto_format(self):
        return format(self.dscto, '.2f')

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['-id']


class Banks(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['-id']


class CtasPay(BaseModel):
    ing = models.ForeignKey(Ingress, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.ing.prov.name

    def toJSON(self):
        item = model_to_dict(self)
        item['ing'] = self.ing.toJSON()
        item['date_joined'] = self.date_joined_format()
        item['end_date'] = self.end_date_format()
        item['total'] = self.total_format()
        item['saldo'] = self.saldo_format()
        return item

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def end_date_format(self):
        return self.end_date.strftime('%Y-%m-%d')

    def total_format(self):
        return format(self.total, '.2f')

    def saldo_format(self):
        return format(self.saldo, '.2f')

    def get_count_quotas(self):
        return self.ctaspaypayments_set.all().count()

    def get_state_display(self):
        if not self.state:
            return 'Pagado'
        return 'Aun debe'

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.ctaspaypayments_set.all():
                i.delete()
        except:
            pass
        super(CtasPay, self).delete()

    class Meta:
        verbose_name = 'Cuenta por pagar'
        verbose_name_plural = 'Cuentas por pagar'
        ordering = ['-id']


class CtasPayPayments(BaseModel):
    cta = models.ForeignKey(CtasPay, on_delete=models.CASCADE)
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE, verbose_name='Banco')
    account_number = models.CharField(max_length=10, null=True, blank=True, verbose_name='Número de cuenta')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')
    details = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')

    def __str__(self):
        return self.bank.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['cta'])
        item['bank'] = self.bank.toJSON()
        item['date_joined'] = self.date_joined_format()
        item['valor'] = self.valor_format()
        item['option'] = True
        return item

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def valor_format(self):
        return format(self.valor, '.2f')

    class Meta:
        verbose_name = 'Pago de Cuenta por pagar'
        verbose_name_plural = 'Pagos de Cuentas por pagar'
        ordering = ['-id']
