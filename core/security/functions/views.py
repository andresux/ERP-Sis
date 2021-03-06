import socket
from core.security.forms import TemplateForm, Company
from datetime import datetime


def system_information(request):
    data = {
        'comp': Company.objects.first(),
        'hostname': socket.gethostname(),
        'menu': get_layout(),
        'template': TemplateForm,
        'localhost': socket.gethostbyname(socket.gethostname()),
        'date_joined': datetime.now(),
    }
    return data


def get_configuration():
    try:
        items = Company.objects.all()
        if items.exists():
            return items[0]
    except:
        pass
    return None


def get_layout():
    objs = Company.objects.filter()
    if objs.exists():
        objs = objs[0]
        if objs.layout == 1:
            return 'vtc_body.html'
        return 'hzt_body.html'
    return 'hzt_body.html'
