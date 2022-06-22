from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from core.security.models import Company
from core.security.decorators.module.decorators import selected_group_session


class HomeView(TemplateView):
    template_name = 'panel.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        selected_group_session(request)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = self.get_context_data()
        comp = Company.objects.filter()
        if comp.exists():
            if comp[0].layout == 1:
                return render(request, 'vtc_panel.html', data)
        return render(request, 'hzt_panel.html', data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['home'] = True
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
