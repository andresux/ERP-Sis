import json
from django.http import JsonResponse, HttpResponse
from django.http.response import HttpResponseNotFound
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from core.college.forms import AssistanceForm, Assistance, AssistanceTeacherForm, TeacherMatter
from core.college.models import ClassRoom, Course, Matter
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
import os
import io
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from datetime import datetime 
import json

# ADMIN
class AssistanceListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Assistance
    template_name = 'assistance/list.html'
    permission_required = 'view_assistance'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Assistance.objects.all().order_by("course")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('assist_create')
        context['title'] = 'Listado de asistencias'
        return context

class AssistanceCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assist_list')
    permission_required = 'add_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nueva asistencia'
        context['action'] = 'add'
        context['add_custom_submit'] = 'add'
        context['folio'] = ''
        
        return context


class AssistanceUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assist_list')
    permission_required = 'change_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

    def validate_data(self):
        data = {'valid': True}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una asistencia'
        context['action'] = 'edit'
        context['add_custom_submit'] = 'edit'
        context['folio'] = list(Assistance.objects.filter(id=self.kwargs['pk']).values_list("folio"))[0][0]
        return context


class AssistanceDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Assistance
    template_name = 'assistance/delete.html'
    success_url = reverse_lazy('assist_list')
    permission_required = 'delete_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Assistance.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación de asistencia'
        context['list_url'] = self.success_url
        return context
    

# TEACHER
class AssistanceTeacherListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Assistance
    template_name = 'assistance/list_teacher.html'
    permission_required = 'view_assistance'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        matters = TeacherMatter.objects.filter(teacher__user_id=self.request.user.id).values_list("period")
        return Assistance.objects.filter(course__period__in=matters).order_by("course")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('assist_teacher_create')
        context['title'] = 'Listado de asistencias'
        return context

class AssistanceTeacherCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceTeacherForm
    success_url = reverse_lazy('assist_teacher_list')
    permission_required = 'add_assistance'
    
    def get_form_kwargs(self):
        kwargs = super(AssistanceTeacherCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user.id
        return kwargs

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nueva asistencia'
        context['action'] = 'add'
        context['add_custom_submit'] = 'add'
        context['folio'] = ''
        
        return context


class AssistanceTeacherUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assist_teacher_list')
    permission_required = 'change_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return super().get_form()

    def validate_data(self):
        data = {'valid': True}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una asistencia'
        context['action'] = 'edit'
        context['add_custom_submit'] = 'edit'
        context['folio'] = list(Assistance.objects.filter(id=self.kwargs['pk']).values_list("folio"))[0][0]
        return context


class AssistanceTeacherDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Assistance
    template_name = 'assistance/delete.html'
    success_url = reverse_lazy('assist_teacher_list')
    permission_required = 'delete_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Assistance.objects.get(pk=self.get_object().id).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación de asistencia'
        context['list_url'] = self.success_url
        return context

# PRINT
class AssistancePrintView(View):
    doc = DocxTemplate(str(os.path.abspath(os.path.dirname(__name__))+'/media/word_templates/asistencia.docx').replace('\\', '/'))    

    levels_education = {
        "1": 'CORTA',
        "2": 'LARGA'
    }

    meses_siglas = {
        "1": 'ENE',
        "2": 'FEB',
        "3": 'MAR',
        "4": 'ABR',
        "5": 'MAY',
        "6": 'JUN',
        "7": 'JUL',
        "8": 'AGO',
        "9": 'SEP',
        "10": 'OCT',
        "11": 'NOV',
        "12": 'DIC'
    }
    
    meses = {
        "1": 'enero',
        "2": 'febrero',
        "3": 'marzo',
        "4": 'abril',
        "5": 'mayo',
        "6": 'junio',
        "7": 'julio',
        "8": 'agosto',
        "9": 'septiembre',
        "10": 'octubre',
        "11": 'noviembre',
        "12": 'diciembre'
    }

    dias = {
        "0": 'lunes',
        "1": 'martes',
        "2": 'miércoles',
        "3": 'jueves',
        "4": 'viernes',
        "5": 'sabado',
        "6": 'domingo',
    }
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        asistencia = list(Assistance.objects.filter(id = self.kwargs["pk"]).values())[0]
        course = list(Course.objects.filter(id = asistencia["course_id"]).values())[0]
        matter = list(Matter.objects.filter(id = asistencia["matter_id"]).values())[0]
        classroom = list(ClassRoom.objects.filter(id = course["classroom_id"]).values())[0]
        
        alumnos = []
        cont = 1;

        json_alumnos = json.loads(asistencia["assistance"])
        for a in json_alumnos.keys():
            alumno = json_alumnos[a]
            alumnos.append({
                    "no":cont,
                    "nacionalidad":alumno["cedula"],
                    "participantes":alumno["nombre"],
                    "a":'X' if alumno['asistencia'] == 'a' else '',
                    "f":'X' if alumno['asistencia'] == 'f' else '',
                    "observacion":alumno["obs"],
            })
            cont += 1
        folder = str(os.path.abspath(os.path.dirname(__name__)))
        imagenes_list = json.loads(asistencia['anexos'])
        imagenes = []
        for i in imagenes_list:
            print((folder+i).replace('\\', '/'))
            imagenes.append(InlineImage(self.doc, (folder+i).replace('\\', '/'), width=Mm(175)))
        
        context = { 
            "duracion" : self.levels_education[str(course["level"])],
            "mes": self.meses_siglas[str(asistencia["date"].month)],
            "anio": str(asistencia["date"].year),
            "fechaAsistencia": self.dias[str(asistencia["date"].weekday())]+", "+str(asistencia["date"].day)+" de "+ self.meses[str(asistencia["date"].month)]+" de "+ str(asistencia["date"].year),
            "horaIni": asistencia["start_hour"],
            "horaFin": asistencia["end_hour"],
            "horasTotalAsignatura": asistencia["total_hours"],
            "nombreCurso": classroom["name"],
            "nombreDocente": asistencia["teacher"],
            "tema": asistencia["subject"],
            "esPresencial": 'X' if asistencia["modality"] == 'Presencial' else '',
            "esVirtual": 'X' if asistencia["modality"] == 'Virtual' else '',
            "esEnVivo": "",
            "mooc": "",
            "via": asistencia["via"],
            "horasPresencialVirtual": asistencia["class_hours"],
            "horasAutonomas": asistencia["self_hours"],
            "horasTotal": str(asistencia["class_hours"])+"/"+str(asistencia["total_hours"]),
            "contenido": asistencia["content"],
            "actividadAprendizaje": [
                asistencia["learning"],     
            ],
            "actividadesAutonomas": [
                asistencia["self_learn"],   
            ],
            "actividadesEvaluacion": [
                asistencia["evaluation"],      
            ],
            "documentosAnexos": [
                asistencia["documents_type"],      
            ],
            "observaciones ": [
                asistencia["observations"],      
            ], 
            "nombreJefe": asistencia["signatures"],
            "nombreCoordinador": asistencia["coordinator"],
            "alumnos": alumnos,
            'imagenes': imagenes
        }
        self.doc.render(context)


        file_name = "generated_doc_"+datetime.now().strftime("%y%m%d_%H%M%S")+"_"+str(self.request.user.id)+'.docx'
        bio = io.BytesIO()
        self.doc.save(bio)
        bio.seek(0)
        response = HttpResponse(
            bio.getvalue(),  # use the stream's contents
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        response["Content-Disposition"] = 'attachment; filename = "'+file_name+'"'
        response["Content-Encoding"] = "UTF-8"
        return response

