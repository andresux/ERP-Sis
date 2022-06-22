import json
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, View
from core.college.forms import FinalReportForm, FinalReportTeacherForm, FinalReport
from core.college.models import Assistance, ClassRoom, Course, TeacherMatter, Notes
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin
import os
import io
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from datetime import datetime 
import json

# ADMIN
class FinalReportCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = FinalReport
    template_name = 'report/final_create.html'
    form_class = FinalReportForm
    success_url = reverse_lazy('home')
    permission_required = 'create_final_report'

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
                self.get_form().save()
                data["id"] = self.model.objects.latest('id').id
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
        context['title'] = 'Nuevo reporte final'
        context['action'] = 'add'        
        return context

# TEACHER
class FinalReportTeacherCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = FinalReport
    template_name = 'report/final_create.html'
    form_class = FinalReportTeacherForm
    success_url = reverse_lazy('home')
    permission_required = 'create_final_report'
    
    def get_form_kwargs(self):
        kwargs = super(FinalReportTeacherCreateView, self).get_form_kwargs()
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
                self.get_form().save()
                data["id"] = self.model.objects.latest('id').id
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

# PRINT
class FinalReportPrintView(View):
    doc = DocxTemplate(str(os.path.abspath(os.path.dirname(__name__))+'/media/word_templates/informe_final.docx').replace('\\', '/'))    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        report = list(FinalReport.objects.filter(id = self.kwargs["pk"]).values())[0]
        course = list(Course.objects.filter(id = report["course_id"]).values())[0]
        classroom = list(ClassRoom.objects.filter(id = course["classroom_id"]).values())[0]
        teacher = list(TeacherMatter.objects.filter(period = course["period_id"]).values("teacher__user__first_name", "teacher__user__last_name"))[0]
        asistencia = list(Assistance.objects.filter(matter = report["matter_id"]).values("assistance"))
        
        alumnos_data = {}
        for a in asistencia:
            json_alumnos = json.loads(a["assistance"])
            for a in json_alumnos.keys():
                alumno = json_alumnos[a]
                if not 'alumno'+str(alumno["id"]) in alumnos_data.keys(): 
                    notas = list(Notes.objects.filter(matr__course__id=report["course_id"], matr__student_id=alumno["id"], ).values("average"))
                    alumnos_data['alumno'+str(alumno["id"])] = {
                        "nacionalidad":alumno["cedula"],
                        "participantes":alumno["nombre"],
                        "asistencia":0,
                        "a":0,
                        "f":0,
                        "nota":notas[0]['average'] if len(notas) > 0 else ''
                    }
                alumnos_data['alumno'+str(alumno["id"])]["asistencia"]+=1
                if alumno["asistencia"] == 'a':
                    alumnos_data['alumno'+str(alumno["id"])]["a"]+=1
                else:
                    alumnos_data['alumno'+str(alumno["id"])]["f"]+=1
        
        count = 1;
        alumnos = []
        for k in alumnos_data.keys():
            alum = alumnos_data[k]
            aprueba = ''
            if alum["nota"] == '':
                aprueba = 'SIN NOTA FINAL'
            elif alum["nota"] >= 7 and (alum["a"]/alum["asistencia"]*100)>= 70:
                aprueba = 'APRUEBA'
            elif alum["nota"] < 7 or (alum["a"]/alum["asistencia"]*100) < 70:
                aprueba = 'REPROBADO'

            alumnos.append({
                "no":str(count),
                "nacionalidad":alum["nacionalidad"],
                "participantes":alum["participantes"],
                "asistencia":str(round(alum["a"]/alum["asistencia"]*100, 2))+"%",
                "nota":alum["nota"],
                "aps":'X' if aprueba == 'APRUEBA' else '',
                "apn":'X' if aprueba == 'REPROBADO' else '',
                "obs":aprueba,
            })
            count+=1

        context = { 
            "docente" : teacher["teacher__user__last_name"]+" "+teacher["teacher__user__first_name"],
            "jefe": report["signatures"],
            "nombreCurso": classroom["name"],
            "modalidad": report["modality"].upper(),
            "via": report["via"].upper(),
            "totalHoras": report["class_hours"] + report["self_hours"],
            "introduccion": report["introduction"],
            "objetivo": report["objective"],
            "especifico": report["specific_objective"],
            "alumnos":alumnos,
            "conclusiones": report["conclutions"],
            "recomendaciones": report["recomendation"],
            "coordinador": report["coordinator"]
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

