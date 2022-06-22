from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models.fields import TextField
from django.forms import *
from .models import *


class MatterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Matter
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'credits': TextInput(attrs={'placeholder': 'Ingrese el numero de horas de la materia o módulo'})
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data

class UnitForm(ModelForm):
    matter = ModelChoiceField(queryset=Matter.objects.filter(),
                                  widget=Select(attrs={'id': 'matter', 'class': 'form-control select', 'style': 'width:100%;'}),
                                  label='Materia', required=True)
    name = CharField(widget=TextInput(attrs={'id': 'name','placeholder': 'Nombre de la Unidad'}), label='Nombre de la Unidad')
    number = CharField(widget=TextInput(attrs={'id': 'number','placeholder': 'Número de unidad'}), label='Nº unidad')
    total_hours = CharField(widget=TextInput(attrs={'id': 'total_hours','placeholder': 'Total horas Unidad'}), label='Total horas Unidad')
    learning_result = CharField(widget=TextInput(attrs={'id': 'learning_result','placeholder': 'Resultados de Aprendizaje'}), label='Resultados de Aprendizaje')
    type_hours = ChoiceField(widget=Select(attrs={'id': 'type_hours','placeholder': 'Tipo de horas'}),choices=[('presenciales','Presenciales'),('virtuales','Virtuales')], label='Tipo de horas')
    class_hours = CharField(widget=TextInput(attrs={'id': 'class_hours','placeholder': 'Horas'}), label='Total horas Presenciales/Virtuales')
    self_hours = CharField(widget=TextInput(attrs={'id': 'self_hours','placeholder': 'Autónomas'}), label='Autónomas')
    
    folios = CharField(widget=HiddenInput(attrs={'id': 'folios','placeholder': 'Folios'}), label='Folios')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Unit
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data

class TypeCourseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = TypeCourse
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class ProfessionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Profession
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'})
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class PeriodForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Period
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'})
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class PersonForm(UserCreationForm):
    first_name = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese sus nombres'}), label='Nombres')
    last_name = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}), label='Apellidos')
    dni = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}), label='Número de cedula',
                    max_length=13)
    email = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su email'}), label='Email')
    gender = ChoiceField(choices=gender, widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
                         label='Genero')
    address = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su dirección'}), label='Dirección')
    mobile = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su teléfono celular'}), label='Teléfono celular',
                       max_length=10)
    conventional = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su teléfono convencional'}),
                             label='Teléfono convencional', max_length=7)
    birthdate = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(attrs={
        'value': datetime.now().strftime('%Y-%m-%d'),
        'id': 'birthdate',
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#birthdate',
    }), label='Fecha de nacimiento')
    # type = ChoiceField(choices=type_pers,
    #                    widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}), label='Tipo')
    profession = ModelChoiceField(queryset=Profession.objects.filter(),
                                  widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
                                  label='Profesión', required=True)
    cvitae = FileField(label='C.Vitae')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']
        del self.fields['username']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'dni', 'email', 'image', 'cvitae')
        exclude = ['user_creation', 'user_updated']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class PersonChangeForm(UserChangeForm):
    first_name = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese sus nombres'}), label='Nombres')
    last_name = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}), label='Apellidos')
    dni = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}), label='Número de cedula',
                    max_length=13)
    email = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su email'}), label='Email')
    gender = ChoiceField(choices=gender, widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
                         label='Genero')
    address = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su dirección'}), label='Dirección')
    mobile = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su teléfono celular'}), label='Teléfono celular',
                       max_length=10)
    conventional = CharField(widget=TextInput(attrs={'placeholder': 'Ingrese su teléfono convencional'}),
                             label='Teléfono convencional', max_length=7)
    birthdate = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(attrs={
        'value': datetime.now().strftime('%Y-%m-%d'),
        'id': 'birthdate',
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#birthdate',
    }), label='Fecha de nacimiento')
    # type = ChoiceField(choices=type_pers,
    #                    widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}), label='Tipo')
    profession = ModelChoiceField(queryset=Profession.objects.filter(),
                                  widget=Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
                                  label='Profesión', required=True)
    cvitae = FileField(label='C.Vitae')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        super(PersonChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        del self.fields['username']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'dni', 'email', 'image', 'cvitae')
        exclude = ['user_creation', 'user_updated']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class CourseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classroom'].widget.attrs['autofocus'] = True

    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'classroom': Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
            'period': Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
            'level': Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class TeacherMatterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit', False)
        super().__init__(*args, **kwargs)
        self.fields['teacher'].widget.attrs['autofocus'] = True
        self.fields['teacher'].queryset = Person.objects.filter(type='docente')
        if edit:
            self.fields['period'].widget.attrs['disabled'] = True
            self.fields['teacher'].widget.attrs['disabled'] = True

    class Meta:
        model = TeacherMatter
        fields = '__all__'
        widgets = {
            'teacher': Select(attrs={'class': 'form-control select2'}),
            'period': Select(attrs={'class': 'form-control select2'}),
        }
        exclude = ['user_updated', 'user_creation', 'date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class MatriculationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs['autofocus'] = True

    class Meta:
        model = Matriculation
        fields = '__all__'
        widgets = {
            'course': Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
        }
        exclude = ['user_updated', 'user_creation', 'date_joined', 'student', 'state']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class MatrStateForm(forms.Form):
    state_matricul = (
        ('', '-------'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )

    state = ChoiceField(choices=state_matricul, widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))


class ClassRoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ClassRoom
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'type_course': Select(attrs={'class': 'form-control select2', 'style': 'width:100%;'}),
            'description': TextInput(attrs={'placeholder': 'Ingrese una Descripción'}),
            'platform_infrastructure': TextInput(attrs={'placeholder': 'Ingrese una plataforma'}),
            'duration': NumberInput(attrs={'placeholder': 'Ingrese las horas que durará el curso'}),
            'minimum_participants': NumberInput(attrs={'placeholder': 'Minimo de participantes'}),
        }
        exclude = ['user_updated', 'user_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class CommentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['autofocus'] = True

    class Meta:
        model = Comments
        fields = '__all__'
        widgets = {
            'message': Textarea(attrs={'placeholder': 'Ingrese su queja o comentario', 'rows': 4, 'cols': 4}),
        }
        exclude = ['user_updated', 'user_creation', 'pers', 'date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class NotesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Notes
        fields = '__all__'
        exclude = ['date_joined']

    course = ChoiceField(choices=[], widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    matters = ChoiceField(choices=[], widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    semester = ChoiceField(choices=semester, widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))


class NoteStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        student_id = kwargs.pop('student_id', 0)
        super().__init__(*args, **kwargs)
        if student_id > 0:
            self.fields['course'].queryset = Matriculation.objects.filter(student_id=student_id)

    course = ModelChoiceField(queryset=None, widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))


class StudentCourseForm(forms.Form):
    course = ModelChoiceField(queryset=Course.objects.all(), widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    teacher = ModelChoiceField(queryset=Person.objects.none(), widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    matter = ModelChoiceField(queryset=Matter.objects.none(), widget=Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass

class AssistanceForm(ModelForm):
    course =  ModelChoiceField(queryset=Course.objects.filter(),
                                  widget=Select(attrs={'id': 'course', 'class': 'form-control select', 'style': 'width:100%;'}),
                                  label='Curso', required=True)
    teacher = CharField(widget=TextInput(attrs={'id': 'teacher','placeholder': 'Docente', 'readonly': 'true'}), label='Docente', required=True)
    coordinator = CharField(widget=TextInput(attrs={'id': 'coordinator','placeholder': 'Coordinadora'}), label='Coordinadora', required=True)
    date = DateField(widget=DateInput(attrs={'id': 'date','placeholder': 'Fecha asistencia', 'value': datetime.now().strftime("%Y-%m-%d"), 'readonly': 'true'}), 
                        label='Fecha asistencia', required=True)
    start_hour = CharField(widget=TextInput(attrs={'id': 'start_hour','placeholder': 'Hora inicio'}), label='Hora inicio', required=True)
    end_hour = CharField(widget=TextInput(attrs={'id': 'end_hour','placeholder': 'Hora fin'}), label='Hora fin', required=True)
    clases = CharField(widget=TextInput(attrs={'id': 'clases','placeholder': 'Número de clases', 'value':'1', 'readonly': 'true'}), label='Clase', required=True)
    total_hours = IntegerField(widget=TextInput(attrs={'id': 'total_hours','placeholder': 'Total horas clase', 'readonly': 'true'}), label='Total horas clase')
    folio = ChoiceFieldNoValidation(widget=Select(attrs={'id': 'folio'}), label='Folio')
    subject = CharField(widget=TextInput(attrs={'id': 'subject','placeholder': 'Tema'}), label='Tema')
    modality = ChoiceField(widget=Select(attrs={'id': 'modality'}),choices=[('Presencial','Presencial'),('Virtual','Virtual')],label='Modalidad')
    via = CharField(widget=TextInput(attrs={'id': 'subject','placeholder': 'Ubicación/Plataforma'}), label='Ubicación/Plataforma')
    class_hours = CharField(widget=TextInput(attrs={'id': 'class_hours','placeholder': 'Horas'}), label='Total horas Presenciales/Virtuales')
    self_hours = IntegerField(widget=TextInput(attrs={'id': 'self_hours','placeholder': 'Total horas autónomas'}), label='Total horas autónomas')
    imparted_hours = IntegerField(widget=TextInput(attrs={'id': 'self_hours','placeholder': 'Total horas impartidas'}), label='Total horas impartidas')
    content = CharField(widget=TextInput(attrs={'id': 'content','placeholder': 'Contenido', 'readonly': 'true'}), label='Contenido')
    learning = CharField(widget=TextInput(attrs={'id': 'learning','placeholder': 'Actividades de aprendizaje', 'readonly': 'true'}), label='Actividades de aprendizaje')
    self_learn = CharField(widget=TextInput(attrs={'id': 'self','placeholder': 'Actividades autónomas', 'readonly': 'true'}), label='Actividades autónomas')
    evaluation = CharField(widget=TextInput(attrs={'id': 'evaluation','placeholder': 'Actividades de evaluación', 'readonly': 'true'}), label='Actividades de evaluación')
    documents_type = CharField(widget=TextInput(attrs={'id': 'documents_type','placeholder': 'Diapositivas u otro medio'}),label='Documentos o anexos')
    observations = CharField(widget=TextInput(attrs={'id': 'observations','placeholder': 'Observaciones'}), label='Observaciones', required=False)
    anexos = CharField(widget=HiddenInput(attrs={'id': 'anexos','placeholder': 'Anexos'}), label='Anexos')
    assistance = CharField(widget=HiddenInput(attrs={'id': 'assistance','placeholder': 'Asistencia'}), label='Asistencia')
    signatures = CharField(widget=TextInput(attrs={'id': 'signatures','placeholder': 'Nombre de jefe/a'}), label='Jefe/a de Capacitación y Consultoría')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset =Course.objects.filter()
        

    class Meta:
        model = Assistance
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class AssistanceTeacherForm(ModelForm):
    course = ModelChoiceField(queryset = Course.objects.filter(),
                        widget=Select(attrs={'id': 'course', 'class': 'form-control select', 'style': 'width:100%;'}),
                        label='Curso', required=True)
    teacher = CharField(widget=TextInput(attrs={'id': 'teacher','placeholder': 'Docente', 'readonly': 'true'}), label='Docente', required=True)
    coordinator = CharField(widget=TextInput(attrs={'id': 'coordinator','placeholder': 'Coordinadora'}), label='Coordinadora', required=True)
    date = DateField(widget=DateInput(attrs={'id': 'date','placeholder': 'Fecha asistencia', 'value': datetime.now().strftime("%Y-%m-%d"), 'readonly': 'true'}), 
                        label='Fecha asistencia', required=True)
    start_hour = CharField(widget=TextInput(attrs={'id': 'start_hour','placeholder': 'Hora inicio'}), label='Hora inicio', required=True)
    end_hour = CharField(widget=TextInput(attrs={'id': 'end_hour','placeholder': 'Hora fin'}), label='Hora fin', required=True)
    clases = CharField(widget=TextInput(attrs={'id': 'clases','placeholder': 'Número de clases', 'value':'1', 'readonly': 'true'}), label='Clase', required=True)
    total_hours = IntegerField(widget=TextInput(attrs={'id': 'total_hours','placeholder': 'Total horas clase', 'readonly': 'true'}), label='Total horas clase')
    folio = ChoiceFieldNoValidation(widget=Select(attrs={'id': 'folio'}), label='Folio')
    subject = CharField(widget=TextInput(attrs={'id': 'subject','placeholder': 'Tema'}), label='Tema')
    modality = ChoiceField(widget=Select(attrs={'id': 'modality'}),choices=[('Presencial','Presencial'),('Virtual','Virtual')],label='Modalidad')
    via = CharField(widget=TextInput(attrs={'id': 'subject','placeholder': 'Ubicación/Plataforma'}), label='Ubicación/Plataforma')
    class_hours = CharField(widget=TextInput(attrs={'id': 'class_hours','placeholder': 'Horas'}), label='Total horas Presenciales/Virtuales')
    self_hours = IntegerField(widget=TextInput(attrs={'id': 'self_hours','placeholder': 'Total horas autónomas'}), label='Total horas autónomas')
    imparted_hours = IntegerField(widget=TextInput(attrs={'id': 'self_hours','placeholder': 'Total horas impartidas'}), label='Total horas impartidas')
    content = CharField(widget=TextInput(attrs={'id': 'content','placeholder': 'Contenido', 'readonly': 'true'}), label='Contenido')
    learning = CharField(widget=TextInput(attrs={'id': 'learning','placeholder': 'Actividades de aprendizaje', 'readonly': 'true'}), label='Actividades de aprendizaje')
    self_learn = CharField(widget=TextInput(attrs={'id': 'self','placeholder': 'Actividades autónomas', 'readonly': 'true'}), label='Actividades autónomas')
    evaluation = CharField(widget=TextInput(attrs={'id': 'evaluation','placeholder': 'Actividades de evaluación', 'readonly': 'true'}), label='Actividades de evaluación')
    documents_type = CharField(widget=TextInput(attrs={'id': 'documents_type','placeholder': 'Diapositivas u otro medio'}),label='Documentos o anexos')
    observations = CharField(widget=TextInput(attrs={'id': 'observations','placeholder': 'Observaciones'}), label='Observaciones', required=False)
    anexos = CharField(widget=HiddenInput(attrs={'id': 'anexos','placeholder': 'Anexos'}), label='Anexos')
    assistance = CharField(widget=HiddenInput(attrs={'id': 'assistance','placeholder': 'Asistencia'}), label='Asistencia')
    signatures = CharField(widget=TextInput(attrs={'id': 'signatures','placeholder': 'Nombre de jefe/a'}), label='Jefe/a de Capacitación y Consultoría')

    def __init__(self, user, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        matters = TeacherMatter.objects.filter(teacher__user_id=user).values_list("period")
        self.fields['course'].queryset =Course.objects.filter(period__in=matters)

    class Meta:
        model = Assistance
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class FinalReportForm(ModelForm):
    course =  ModelChoiceField(queryset=Course.objects.filter(),
                                  widget=Select(attrs={'id': 'course', 'class': 'form-control select', 'style': 'width:100%;'}),
                                  label='Curso', required=True)
    coordinator = CharField(widget=TextInput(attrs={'id': 'coordinator','placeholder': 'Coordinador'}), label='Coordinador', required=True)
    
    modality = ChoiceField(widget=Select(attrs={'id': 'modality'}),choices=[('Presencial','Presencial'),('Virtual','Virtual')],label='Modalidad')
    via = CharField(widget=TextInput(attrs={'id': 'subject','placeholder': 'Ubicación/Plataforma'}), label='Ubicación/Plataforma')
    
    class_hours = CharField(widget=TextInput(attrs={'id': 'class_hours','placeholder': 'Horas'}), label='Total horas Presenciales/Virtuales')
    self_hours = IntegerField(widget=TextInput(attrs={'id': 'self_hours','placeholder': 'Total horas autónomas'}), label='Total horas autónomas')
    
    introduction = CharField(widget=Textarea(attrs={'id': 'introduction','placeholder': 'Introducción'}), label='Introducción')
    objective = CharField(widget=Textarea(attrs={'id': 'objective','placeholder': 'Objetivo'}), label='Objetivo')
    specific_objective = CharField(widget=Textarea(attrs={'id': 'specific_objective','placeholder': 'Objetivo específico'}), label='Objetivo específico')
    conclutions = CharField(widget=Textarea(attrs={'id': 'conclutions','placeholder': 'Conclusiones'}), label='Conclusiones')
    recomendation = CharField(widget=Textarea(attrs={'id': 'recomendation','placeholder': 'Recomendaciones'}), label='Recomendaciones')
    signatures = CharField(widget=TextInput(attrs={'id': 'signatures','placeholder': 'Nombre de jefe/a'}), label='Jefe/a de Capacitación y Consultoría')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset =Course.objects.filter()
        

    class Meta:
        model = FinalReport
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class FinalReportTeacherForm(ModelForm):
    course =  ModelChoiceField(queryset=Course.objects.filter(),
                                  widget=Select(attrs={'id': 'course', 'class': 'form-control select', 'style': 'width:100%;'}),
                                  label='Curso', required=True)
    coordinator = CharField(widget=TextInput(attrs={'id': 'coordinator','placeholder': 'Coordinador'}), label='Coordinador', required=True)
    
    modality = ChoiceField(widget=Select(attrs={'id': 'modality'}),choices=[('Presencial','Presencial'),('Virtual','Virtual')],label='Modalidad')
    via = CharField(widget=TextInput(attrs={'id': 'subject','placeholder': 'Ubicación/Plataforma'}), label='Ubicación/Plataforma')
    
    class_hours = CharField(widget=TextInput(attrs={'id': 'class_hours','placeholder': 'Horas'}), label='Total horas Presenciales/Virtuales')
    self_hours = IntegerField(widget=TextInput(attrs={'id': 'self_hours','placeholder': 'Total horas autónomas'}), label='Total horas autónomas')
    
    introduction = CharField(widget=Textarea(attrs={'id': 'introduction','placeholder': 'Introducción'}), label='Introducción')
    objective = CharField(widget=Textarea(attrs={'id': 'objective','placeholder': 'Objetivo'}), label='Objetivo')
    specific_objective = CharField(widget=Textarea(attrs={'id': 'specific_objective','placeholder': 'Objetivo específico'}), label='Objetivo específico')
    conclutions = CharField(widget=Textarea(attrs={'id': 'conclutions','placeholder': 'Conclusiones'}), label='Conclusiones')
    recomendation = CharField(widget=Textarea(attrs={'id': 'recomendation','placeholder': 'Recomendaciones'}), label='Recomendaciones')
    signatures = CharField(widget=TextInput(attrs={'id': 'signatures','placeholder': 'Nombre de jefe/a'}), label='Jefe/a de Capacitación y Consultoría')
 
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        matters = TeacherMatter.objects.filter(teacher__user_id=user).values_list("period")
        self.fields['course'].queryset =Course.objects.filter(period__in=matters)
        

    class Meta:
        model = FinalReport
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data