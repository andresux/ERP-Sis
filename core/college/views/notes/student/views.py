import json
import os
from io import BytesIO

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from xhtml2pdf import pisa

from config.settings import MEDIA_URL, MEDIA_ROOT
from core.college.forms import Notes, NoteStudentForm, Matter, Matriculation, Person
from core.home.choices import semester
from core.security.mixins import AccessModuleMixin
from core.security.models import Company


class NotesListView(AccessModuleMixin, TemplateView):
    model = Notes
    template_name = 'notes/student/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_notes':
                data = []
                id = int(request.POST['id'])
                matr = Matriculation.objects.get(pk=id)
                for n in matr.notes_set.all():
                    data.append(n.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Calificaciones'
        context['form'] = NoteStudentForm(student_id=self.request.user.person.id)
        return context


class NotesPrintView(View):
    success_url = reverse_lazy('notes_student_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            if Matriculation.objects.filter(pk=int(self.kwargs['pk'])).exists():
                template = get_template('notes/student/pdf.html')
                context = {
                    'comp': Company.objects.first(),
                    'matriculation': Matriculation.objects.get(pk=int(self.kwargs['pk'])),
                }
                html = template.render(context)
                result = BytesIO()
                links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
                pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)
                return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)
