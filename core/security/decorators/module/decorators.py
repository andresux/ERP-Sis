from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from config.settings import HOME
from core.security.models import Module


def access_module(f):
    def access(*args, **kwargs):
        request = args[0]
        try:
            selected_group_session(request)
            id = get_group_session(request)
            if request.user.is_authenticated:
                url_absolute = get_absolute_path(id, request.path)
                request.session['path'] = request.path
                modules = Module.objects.filter(groupmodule__groups_id__in=[id], is_active=True, url=url_absolute,
                                                is_visible=True)
                print(modules)
                if modules.exists():
                    if modules.filter(type_id__isnull=True).exists():
                        request.session['module'] = modules[0]
                        return f(request)
                    elif modules.filter(type__is_active=True).exists():
                        request.session['module'] = modules[0]
                        return f(request)
        except Exception as e:
            return f(request)
        return HttpResponseRedirect(HOME+"dashboard/")

    return access


def selected_group_session(request):
    try:
        groups = request.user.groups.all()
        if groups:
            groups_first = groups[0]
            if 'group' in request.session:
                groups_first = request.session['group']
            request.session['group'] = groups_first
            del request.session['module']
    except:
        pass


def get_group(id):
    try:
        objs = Group.objects.filter(id=id)
        if objs.exists():
            return objs[0]
        return None
    except:
        return None


def get_group_session(request):
    try:
        return int(request.session['group'].id)
    except:
        return 0


def get_absolute_path(id, url):
    search = Module.objects.filter(groupmodule__groups_id=id, is_active=True, is_visible=True)
    for m in search:
        if url == m.url:
            return m.url
    for m in search:
        if url.__contains__(m.url):
            return m.url
    return ""


def get_module_session(group_id, url):
    try:
        return Module.objects.get(groupmodule__groups_id=group_id, url=url, is_active=True)
    except:
        return None
