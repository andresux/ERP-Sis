from datetime import time
from random import randint

from config.wsgi import *
from core.college.models import *
from core.rrhh.models import *
from core.ingress.models import *
#
# for d in AssistanceDet.objects.filter():
#     d.hour = time(7, randint(0, 20))
#     d.save()