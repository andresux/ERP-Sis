import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from core.college.forms import Notes, NotesForm, Course, TeacherMatterDet, Matriculation
from core.home.choices import partial, semester
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class NotesListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Notes
    template_name = 'notes/teacher/list.html'
    permission_required = 'view_notes'

    def get_queryset(self):
        id = self.request.user.person.id
        teacher_ids = TeacherMatterDet.objects.filter(teacher_mat__teacher_id=id).values_list('id', flat=True)
        return Course.objects.filter(coursemat__teachermatterdet__in=teacher_ids).distinct()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_notes':
                 data = []
                 for n in Notes.objects.filter(teach_cours_mat_id=request.POST['id']):
                     data.append(n.toJSON())
            elif action == 'remove_notes':
                Notes.objects.filter(teach_cours_mat_id=request.POST['id']).delete()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('notes_teacher_create')
        context['title'] = 'Listado de Calificaciones'
        return context


class NotesCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Notes
    template_name = 'notes/teacher/create.html'
    form_class = NotesForm
    success_url = reverse_lazy('notes_teacher_list')
    permission_required = 'add_notes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_courses(self):
        data = [{'id': '', 'text': '-----------'}]
        try:
            id = self.request.user.person.id
            teacher_ids = TeacherMatterDet.objects.filter(teacher_mat__teacher_id=id).values_list('id', flat=True)
            courses = Course.objects.filter(coursemat__teachermatterdet__in=teacher_ids).distinct()
            for course in courses:
                data.append({
                    'id': course.id,
                    'text': course.__str__(),
                    'data': [t.toJSON() for t in TeacherMatterDet.objects.filter(teacher_mat__teacher_id=id,
                                                                                 course_mat__course_id=course.id)]
                })
        except:
            pass
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                with transaction.atomic():
                    itemsjson = json.loads(request.POST['items'])
                    teach_cours_mat_id = itemsjson['matter']
                    for item in itemsjson['notes']:
                        search = Notes.objects.filter(teach_cours_mat_id=teach_cours_mat_id, matr_id=item['matr']['id'])
                        notes = Notes()
                        if search.exists():
                            notes = search[0]
                        notes.teach_cours_mat_id = teach_cours_mat_id
                        notes.matr_id = item['matr']['id']
                        notes.lesson1 = float(item['notes']['lesson1'])
                        notes.lesson2 = float(item['notes']['lesson2'])
                        notes.lesson3 = float(item['notes']['lesson3'])
                        notes.lesson4 = float(item['notes']['lesson4'])
                        notes.exam = float(item['notes']['exam'])
                        notes.average = (float(notes.lesson1) + float(notes.lesson2) + float(notes.lesson3) + float(notes.lesson4) + float(notes.exam)) / 5
                        notes.save()
            elif action == 'search_students_notes':
                data = []
                course_id = request.POST['course']
                matter_id = request.POST['matter']
                for i in Matriculation.objects.filter(course_id=course_id):
                    item = {}
                    item['matr'] = i.toJSON()
                    notes = i.notes_set.filter(teach_cours_mat_id=matter_id)
                    valors = {
                        'lesson1': 0.00,
                        'lesson2': 0.00,
                        'lesson3': 0.00,
                        'lesson4': 0.00,
                        'exam': 0.00,
                        'average': 0.00,
                    }
                    if notes.exists():
                        notes = notes[0]
                        valors['lesson1'] = format(notes.lesson1, '.2f')
                        valors['lesson2'] = format(notes.lesson2, '.2f')
                        valors['lesson3'] = format(notes.lesson3, '.2f')
                        valors['lesson4'] = format(notes.lesson4, '.2f')
                        valors['exam'] = format(notes.exam, '.2f')
                        valors['average'] = format(notes.average, '.2f')
                    item['notes'] = valors
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Calificación'
        context['action'] = 'add'
        context['courses'] = self.get_courses()
        return context
