from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime 
import os
import pathlib
from core.college.forms import CourseMat, Unit, TeacherMatter, Matriculation
import json

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        relative_path = '/media/files/'+datetime.now().strftime('%Y/%m/%d')
        folder = str(os.path.abspath(os.path.dirname(__name__))+relative_path).replace('\\', '/')
        if not os.path.exists(folder):
            os.makedirs(folder)
        myfile = request.FILES['file']
        fs = FileSystemStorage(folder)
        basename = "file"
        suffix = datetime.now().strftime("%y%m%d_%H%M%S")
        filename_new = "".join([basename, suffix, pathlib.Path(myfile.name).suffix])
        filename = fs.save(filename_new, myfile)
        return JsonResponse(status=200, data={
            "status": "success", 
            "message": "Archivo subido exitosamente",
            "url": relative_path +"/"+ filename
        })
    return JsonResponse(status=500, data={"status": "failed", "message": "Ocurrio un error al subir el archivo"})

@csrf_protect
def get_matters_by_course(request):
    if request.method == 'POST':
        course = json.loads(request.body)["course"]
        curso_materias = list(CourseMat.objects.filter(course=course).values_list("mat__id","mat__name","course__period"))
        data = []
        folios = {}
        for i in curso_materias:
            folios_unit = list(Unit.objects.filter(matter=i[0]).values_list("folios","total_hours"))
            for f in folios_unit:
                folios["mat-"+str(i[0])] = {}
                folios["mat-"+str(i[0])]["lista"] = json.loads(f[0])
                folios["mat-"+str(i[0])]["horas"] = f[1]
            teacher = list(TeacherMatter.objects.filter(period = i[2]).values_list("teacher__user__first_name", "teacher__user__last_name"))    
            students = list(Matriculation.objects.filter(course_id=course).values_list("student__id", "student__user__first_name", "student__user__last_name", "student__user__dni").order_by('student__user__last_name'))
            data.append({
                "mat_id":i[0], 
                "mat_name":i[1], 
                "teacher":teacher[0],
                "students":students
            });
        return JsonResponse(status=200, data={"status": "success", "data": data, "folios":folios})
    return JsonResponse(status=500, data={"status": "failed", "message": "Ocurrio un error al subir el archivo"})