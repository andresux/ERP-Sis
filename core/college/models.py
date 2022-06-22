from django.db import models
from django.forms import model_to_dict
from datetime import datetime

import config.settings
from config.settings import MEDIA_URL
from core.home.choices import type_pers, gender, levels_education, state_matricul, partial, semester
from core.models import BaseModel
from core.user.models import User
import json

class TypeCourse(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Curso'
        verbose_name_plural = 'Tipo de Curso'
        ordering = ['-id']


class Matter(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    credits = models.IntegerField(verbose_name='Horas de materia')
    silabus = models.FileField(upload_to='silabus/%Y/%m/%d', null=True, blank=True, verbose_name='silabo de materia')

    def __str__(self):
        return self.name

    def get_silabus(self):
        if self.silabus:
            return f"{config.settings.MEDIA_URL}{self.silabus}"
        return ''

    def toJSON(self):
        item = model_to_dict(self)
        item['silabus'] = self.get_silabus()
        return item

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['-id']
# mustrame cual modeos?

class Unit(BaseModel):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, verbose_name='Materia')
    name = models.TextField(verbose_name='Nombre de la Unidad')
    number = models.IntegerField(verbose_name='Nº unidad')
    total_hours = models.IntegerField(verbose_name='Total horas Unidad')
    learning_result = models.TextField(verbose_name='Resultados de Aprendizaje')
    type_hours = models.TextField(verbose_name='Tipo de horas')
    class_hours = models.IntegerField(verbose_name='Horas presenciales o virtuales')
    self_hours = models.IntegerField(verbose_name='Autónomas')

    folios = models.TextField(verbose_name='Folios');
    
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['-id']

class Profession(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Profesión'
        verbose_name_plural = 'Profesiones'
        ordering = ['-id']


class Person(BaseModel):
    prof = models.ForeignKey(Profession, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Rol')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(choices=type_pers, max_length=50, verbose_name='Tipo')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono Celular')
    conventional = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono Convencional')
    gender = models.IntegerField(choices=gender, default=1, verbose_name='Sexo')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de Nacimiento')
    cvitae = models.FileField(upload_to='cvitae/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def get_cvitae(self):
        return '{}{}'.format(MEDIA_URL, self.cvitae)

    def get_gender_letter(self):
        return self.get_gender_display()[0]

    def toJSON(self):
        item = model_to_dict(self, exclude=['cvitae'])
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate_format()
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        if self.prof:
            item['prof'] = self.prof.toJSON()
            item['cvitae'] = self.get_cvitae()
        return item

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['-id']


class Period(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        ordering = ['-id']


class ClassRoom(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    type_course = models.ForeignKey(TypeCourse, on_delete=models.PROTECT, verbose_name='Tipo de Curso')
    description = models.CharField(max_length=150, verbose_name='Descripción')
    platform_infrastructure = models.CharField(max_length=150, verbose_name='Plataformas')
    duration = models.IntegerField(verbose_name='Horas de Duración')
    minimum_participants = models.IntegerField(verbose_name='Minimo de participantes')
    plancurso = models.FileField(upload_to='plancurso/%Y/%m/%d', null=True, blank=True, verbose_name='Plan de Curso')

    def __str__(self):
        return self.name

    def get_plancurso(self):
        if self.plancurso:
            return f"{config.settings.MEDIA_URL}{self.plancurso}"
        return ''

    def toJSON(self):
        item = model_to_dict(self)
        item['plancurso'] = self.get_plancurso()
        item['type_course'] = self.type_course.toJSON()
        return item

    class Meta:
        verbose_name = 'Sala de clase'
        verbose_name_plural = 'Salas de clase'
        ordering = ['-id']


class Course(BaseModel):
    date_joined = models.DateField(default=datetime.now)
    level = models.IntegerField(choices=levels_education, default=1)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    def __str__(self):
        return '{} / {} / {}'.format(self.classroom.name, self.get_level_display(), self.period.name)

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def get_matters_prof(self, id):
        return TeacherMatterDet.objects.filter(teacher_mat__teacher_id=id, course_mat__course_id=self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined_format()
        item['period'] = self.period.toJSON()
        item['classroom'] = self.classroom.toJSON()
        item['level'] = self.get_level_display().upper()
        return item

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-id']


class CourseMat(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mat = models.ForeignKey(Matter, on_delete=models.CASCADE)

    def __str__(self):
        return self.mat.name

    def toJSON(self):
        item = model_to_dict(self)
        item['course'] = self.course.toJSON()
        item['mat'] = self.mat.toJSON()
        return item

    class Meta:
        verbose_name = 'Curso Det'
        verbose_name_plural = 'Cursos Det'
        ordering = ['-id']


class TeacherMatter(BaseModel):
    teacher = models.ForeignKey(Person, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)

    def __str__(self):
        return self.period.name

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['teacher'] = self.teacher.toJSON()
        item['date_joined'] = self.date_joined_format()
        return item

    class Meta:
        verbose_name = 'Docente Materia'
        verbose_name_plural = 'Docente Materias'
        ordering = ['-id']


class TeacherMatterDet(BaseModel):
    teacher_mat = models.ForeignKey(TeacherMatter, on_delete=models.CASCADE)
    course_mat = models.ForeignKey(CourseMat, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_mat.mat.name

    def toJSON(self):
        item = model_to_dict(self)
        item['course_mat'] = self.course_mat.toJSON()
        item['teacher_mat'] = self.teacher_mat.toJSON()
        return item

    class Meta:
        verbose_name = 'Docente Curso Det'
        verbose_name_plural = 'Docente Cursos Det'
        ordering = ['-id']


class Matriculation(BaseModel):
    date_joined = models.DateField(default=datetime.now)
    student = models.ForeignKey(Person, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    state = models.CharField(choices=state_matricul, default='proceso', max_length=50)

    def __str__(self):
        return self.course.__str__()

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['student'] = self.student.toJSON()
        item['course'] = self.course.toJSON()
        item['date_joined'] = self.date_joined_format()
        return item

    class Meta:
        verbose_name = 'Matriculacion'
        verbose_name_plural = 'Matriculaciones'
        ordering = ['-id']


class Notes(models.Model):
    # semester = models.IntegerField(default=1, choices=semester)
    date_joined = models.DateField(default=datetime.now)
    matr = models.ForeignKey(Matriculation, on_delete=models.CASCADE)
    teach_cours_mat = models.ForeignKey(TeacherMatterDet, on_delete=models.CASCADE)
    lesson1 = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    lesson2 = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    lesson3 = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    lesson4 = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    exam = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    average = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)

    def __str__(self):
        return self.matr.course.classroom.name

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['matr'] = self.matr.toJSON()
        item['teach_cours_mat'] = self.teach_cours_mat.toJSON()
        item['lesson1'] = format(self.lesson1, '.2f')
        item['lesson2'] = format(self.lesson2, '.2f')
        item['lesson3'] = format(self.lesson3, '.2f')
        item['lesson4'] = format(self.lesson4, '.2f')
        item['exam'] = format(self.exam, '.2f')
        item['average'] = format(self.average, '.2f')
        item['date_joined'] = self.date_joined_format()
        return item

    class Meta:
        verbose_name = 'Notas'
        verbose_name_plural = 'Notas'
        ordering = ['-id']


class Comments(BaseModel):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    pers = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Persona')
    message = models.CharField(max_length=500, verbose_name='Comentario')

    def __str__(self):
        return self.message

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined_format()
        item['pers'] = self.pers.toJSON()
        return item

    class Meta:
        verbose_name = 'Queja'
        verbose_name_plural = 'Quejas'
        ordering = ['-id']


class Assistance(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    matter =models.ForeignKey(Matter, on_delete=models.CASCADE, verbose_name='Materia')
    teacher = models.TextField(max_length=150,verbose_name='Docente')
    coordinator = models.TextField(max_length=150,verbose_name='Coordinador')
    date = models.DateField(verbose_name='Fecha asistencia')
    start_hour = models.TextField(max_length=15,verbose_name='Hora inicio')
    end_hour = models.TextField(max_length=15,verbose_name='Hora fin')
    clases = models.IntegerField(verbose_name='Clase')
    total_hours = models.IntegerField(verbose_name='Total horas clase')
    folio = models.TextField(max_length=250,verbose_name='Folio')
    subject = models.CharField(max_length =150,verbose_name='Tema')
    modality = models.CharField(max_length=150,verbose_name='Modalidad')
    via = models.CharField(max_length=150,verbose_name='Ubicación/Plataforma')
    class_hours = models.IntegerField(verbose_name='Horas presenciales o virtuales')
    self_hours = models.IntegerField(verbose_name='Total horas autónomas')
    imparted_hours = models.IntegerField(verbose_name='Total horas impartidas')
    content = models.CharField(max_length=500,verbose_name='Contenido')
    learning = models.CharField(max_length=500,verbose_name='Actividades de aprendizaje')
    self_learn = models.CharField(max_length=500,verbose_name='Actividades autónomas')
    evaluation = models.CharField(max_length=500,verbose_name='Actividades de evaluación')
    documents_type = models.CharField(max_length=150,verbose_name='Documentos o anexos')
    observations = models.CharField(max_length=500,verbose_name='Observaciones', blank=True, null=True)
    anexos = models.TextField(verbose_name='Anexos')
    assistance = models.TextField(verbose_name='Asistencia')
    signatures = models.TextField(verbose_name='Firmas')
    
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-id']


class FinalReport(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    matter =models.ForeignKey(Matter, on_delete=models.CASCADE, verbose_name='Materia')
    modality = models.TextField(max_length=5000,verbose_name='Modalidad', blank=True, null=True)
    coordinator = models.TextField(max_length=150,verbose_name='Coordinador')
    via = models.CharField(max_length=150,verbose_name='Ubicación/Plataforma')
    class_hours = models.IntegerField(verbose_name='Horas presenciales o virtuales')
    self_hours = models.IntegerField(verbose_name='Total horas autónomas')
    introduction = models.TextField(max_length=5000,verbose_name='Introducción', blank=True, null=True)
    objective = models.TextField(max_length=5000,verbose_name='Objetivo', blank=True, null=True)
    specific_objective = models.TextField(max_length=5000,verbose_name='Objetivo específico', blank=True, null=True)
    conclutions = models.TextField(max_length=5000,verbose_name='Conclusiones', blank=True, null=True)
    recomendation = models.TextField(max_length=5000,verbose_name='Recomendaciones', blank=True, null=True)
    signatures = models.TextField(verbose_name='Jefe de capacitacion')
    
    def __str__(self):
        obj = model_to_dict(self)
        return str(obj["id"])

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Reporte Final'
        verbose_name_plural = 'Reportes Finales'
        ordering = ['-id']

