# -*- codign: utf-8 -*-
import os
import random
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import UserManager
from config.settings import MEDIA_URL, STATIC_URL
import uuid
from django.forms.models import model_to_dict
import unicodedata


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Username', max_length=20, unique=True)
    first_name = models.CharField(verbose_name='Nombres', max_length=255)
    last_name = models.CharField(verbose_name='Apellidos', max_length=255)
    dni = models.CharField(max_length=13, unique=True, verbose_name='Cédula o RUC')
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')
    image = models.ImageField(upload_to='users/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_change_password = models.BooleanField(default=False)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True, default=uuid.uuid4, unique=True)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['last_login'] = self.last_login_format()
        item['date_joined'] = self.date_joined_format()
        item['groups'] = [{'id': i.id, 'name': i.name} for i in self.groups.all()]
        # item['access_users'] = self.get_access_users()
        return item

    def get_teacher(self):
        try:
            return self.person.contracts_set.all()
        except:
            return None

    def take_assistance(self):
        from core.rrhh.models import AssistanceDet
        teacher = self.get_teacher()
        if teacher is not None:
            if teacher.exists():
                teacher = teacher[0]
                year = datetime.now().year
                month = datetime.now().month
                day = datetime.now().day
                return AssistanceDet.objects.filter(assist__year=year, assist__month=month, assist__day=day,
                                                    cont_id=teacher.id).exists()
        return True

    def last_login_format(self):
        if self.last_login:
            return self.last_login.date().strftime('%Y-%m-%d')
        return None

    def generate_token(self):
        return uuid.uuid4()

    def generate_username(self):
        names = self.get_full_name().split(' ')
        last_name = names[2]
        while len(last_name) >= 11:
            last_name = last_name[0:round(len(last_name) / 2)]
        username = '{}{}{}'.format(names[0][0], last_name, names[3][0])
        username = ''.join(
            (c for c in unicodedata.normalize('NFD', username) if unicodedata.category(c) != 'Mn')).lower()
        username_generator = username
        cont = 1
        while User.objects.filter(username=username_generator):
            username_generator = '{}{}'.format(username, cont)
            cont += 1
        return username_generator

    def generate_pwd(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7']
        pwd = '{}{}{}'.format(self.dni, ''.join(random.choices(letters, k=3)), ''.join(random.choices(numbers, k=3)))
        return pwd

    def get_access_users(self):
        from core.security.models import AccessUsers
        data = []
        for i in AccessUsers.objects.filter(user_creation_id=self.id):
            data.append(i.toJSON())
        return data

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/default/user.png')

    def remove_img(self):
        try:
            os.remove(self.image.path)
        except:
            pass

    def delete(self, using=None, keep_parents=False):
        self.remove_img()
        super(User, self).delete()

    def get_groups(self):
        data = []
        for i in self.groups.all():
            data.append({'id': i.id, 'name': i.name})
        return data

    def __str__(self):
        return self.get_full_name(), self.groups.all()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']
