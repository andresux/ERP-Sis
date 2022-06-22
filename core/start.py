import random
from random import randint

from config.wsgi import *
from core.ingress.models import Banks
from core.security.models import *
from core.college.models import *
from core.rrhh.models import *
#
# for u in User.objects.filter(groups__name__in=['Estudiante']):
#     numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#     if not hasattr(u, 'person'):
#         person = Person()
#         person.user_id = u.id
#         person.type = 'estudiante'
#         person.address = 'Milagro'
#         person.mobile = ''.join(random.choices(numbers, k=10))
#         person.conventional = ''.join(random.choices(numbers, k=7))
#         person.save()
#         print('Guardado {}'.format(person.id))
