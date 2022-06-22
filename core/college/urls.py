from django.urls import path

from core.college.views.unit.views import *
from .views.matter.views import *
from .views.profession.views import *
from .views.period.views import *
from .views.person.views import *
from .views.course.views import *
from .views.teacher.views import *
from .views.teacher_matter.views import *
from .views.class_room.views import *
from .views.assistance.views import *
from .views.report.views import *
import core.college.views.matriculation.student.views as mat_student
import core.college.views.matriculation.admin.views as mat_admin
import core.college.views.comments.student.views as comm_student
import core.college.views.comments.admin.views as comm_admin
import core.college.views.notes.teacher.views as notes_teacher
import core.college.views.notes.student.views as notes_student
from core.college.views.student.views import *
from core.college.views.type_course.views import *
from core.college.views.student_course.views import *
from core.college.views.api import views as api_adm

urlpatterns = [
    # student_course
    path('student/course/admin/', StudentCourseAdminListView.as_view(), name='student_course_admin'),
    path('student/course/teacher/', StudentCourseTeacherListView.as_view(), name='student_course_teacher'),
    # type course
    path('type/course/', TypeCourseListView.as_view(), name='type_course_list'),
    path('type/course/add/', TypeCourseCreateView.as_view(), name='type_course_create'),
    path('type/course/update/<int:pk>/', TypeCourseUpdateView.as_view(), name='type_course_update'),
    path('type/course/delete/<int:pk>/', TypeCourseDeleteView.as_view(), name='type_course_delete'),
    # matter
    path('matter/', MatterListView.as_view(), name='matter_list'),
    path('matter/add/', MatterCreateView.as_view(), name='matter_create'),
    path('matter/update/<int:pk>/', MatterUpdateView.as_view(), name='matter_update'),
    path('matter/delete/<int:pk>/', MatterDeleteView.as_view(), name='matter_delete'),
    # units
    path('unit/', UnitListView.as_view(), name='unit_list'),
    path('unit/<int:pk>/', UnitListMatterView.as_view(), name='unit_list_matter'),
    path('unit/add/', UnitCreateView.as_view(), name='unit_create'),
    path('unit/update/<int:pk>/', UnitUpdateView.as_view(), name='unit_update'),
    path('unit/delete/<int:pk>/', UnitDeleteView.as_view(), name='unit_delete'),
    # assistance
    path('assist/', AssistanceListView.as_view(), name='assist_list'),
    path('assist/add/', AssistanceCreateView.as_view(), name='assist_create'),
    path('assist/update/<int:pk>/', AssistanceUpdateView.as_view(), name='assist_update'),
    path('assist/delete/<int:pk>/', AssistanceDeleteView.as_view(), name='assist_delete'),
    path('assist/print/<int:pk>/', AssistancePrintView.as_view(), name='assist_print'), 
    # assistance teacher
    path('teacher/assist/', AssistanceTeacherListView.as_view(), name='assist_teacher_list'),
    path('teacher/assist/add/', AssistanceTeacherCreateView.as_view(), name='assist_teacher_create'),
    path('teacher/assist/update/<int:pk>/', AssistanceTeacherUpdateView.as_view(), name='assist_teacher_update'),
    path('teacher/assist/delete/<int:pk>/', AssistanceTeacherDeleteView.as_view(), name='assist_teacher_delete'),
    # profession
    path('profession/', ProfessionListView.as_view(), name='profession_list'),
    path('profession/add/', ProfessionCreateView.as_view(), name='profession_create'),
    path('profession/update/<int:pk>/', ProfessionUpdateView.as_view(), name='profession_update'),
    path('profession/delete/<int:pk>/', ProfessionDeleteView.as_view(), name='profession_delete'),
    # period
    path('period/', PeriodListView.as_view(), name='period_list'),
    path('period/add/', PeriodCreateView.as_view(), name='period_create'),
    path('period/update/<int:pk>/', PeriodUpdateView.as_view(), name='period_update'),
    path('period/delete/<int:pk>/', PeriodDeleteView.as_view(), name='period_delete'),
    # class_room
    path('class/room/', ClassRoomListView.as_view(), name='class_room_list'),
    path('class/room/add/', ClassRoomCreateView.as_view(), name='class_room_create'),
    path('class/room/update/<int:pk>/', ClassRoomUpdateView.as_view(), name='class_room_update'),
    path('class/room/delete/<int:pk>/', ClassRoomDeleteView.as_view(), name='class_room_delete'),
    # person
    path('teacher/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/add/', TeacherCreateView.as_view(), name='teacher_create'),
    path('teacher/update/<int:pk>/', TeacherUpdateView.as_view(), name='teacher_update'),
    path('teacher/delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher_delete'),
    # student
    path('student/', StudentListView.as_view(), name='student_list'),
    path('student/add/', StudentCreateView.as_view(), name='student_create'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('student/delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    # course
    path('course/', CourseListView.as_view(), name='course_list'),
    path('course/add/', CourseCreateView.as_view(), name='course_create'),
    path('course/update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('course/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
    # teacher_matter
    path('teacher/matter/', TeacherMatterListView.as_view(), name='teacher_matter_list'),
    path('teacher/matter/add/', TeacherMatterCreateView.as_view(), name='teacher_matter_create'),
    path('teacher/matter/delete/<int:pk>/', TeacherMatterDeleteView.as_view(), name='teacher_matter_delete'),
    path('teacher/matter/update/<int:pk>/', TeacherMatterUpdateView.as_view(), name='teacher_matter_update'),
    # matriculation_student
    path('matriculation/student/', mat_student.MatriculationListView.as_view(), name='matriculation_student_list'),
    path('matriculation/student/add/', mat_student.MatriculationCreateView.as_view(),
         name='matriculation_student_create'),
    path('matriculation/student/update/<int:pk>/', mat_student.MatriculationUpdateView.as_view(),
         name='matriculation_student_update'),
    path('matriculation/student/delete/<int:pk>/', mat_student.MatriculationDeleteView.as_view(),
         name='matriculation_student_delete'),
    # matriculation_admin
    path('matriculation/admin/', mat_admin.MatriculationListView.as_view(), name='matriculation_admin_list'),
    path('matriculation/admin/delete/<int:pk>/', mat_admin.MatriculationDeleteView.as_view(),
         name='matriculation_admin_delete'),
    # comments_student
    path('comments/student/', comm_student.CommentsListView.as_view(), name='comments_student_list'),
    path('comments/student/add/', comm_student.CommentsCreateView.as_view(), name='comments_student_create'),
    path('comments/student/update/<int:pk>/', comm_student.CommentsUpdateView.as_view(),
         name='comments_student_update'),
    path('comments/student/delete/<int:pk>/', comm_student.CommentsDeleteView.as_view(),
         name='comments_student_delete'),
    # comments_admin
    path('comments/admin/', comm_admin.CommentsListView.as_view(), name='comments_admin_list'),
    path('comments/admin/delete/<int:pk>/', comm_admin.CommentsDeleteView.as_view(), name='comments_admin_delete'),
    # notes_teacher
    path('notes/teacher/', notes_teacher.NotesListView.as_view(), name='notes_teacher_list'),
    path('notes/teacher/add/', notes_teacher.NotesCreateView.as_view(), name='notes_teacher_create'),
    # notes_student
    path('notes/student/', notes_student.NotesListView.as_view(), name='notes_student_list'),
    path('notes/student/print/<int:pk>/', notes_student.NotesPrintView.as_view(), name='notes_student_print'),
    # api
    path('api/upload/', api_adm.upload_file, name='upload_file'),
    path('api/get_matters_by_course', api_adm.get_matters_by_course, name='get_matters_by_course'),    
    # Reports
    path('report/final/', FinalReportCreateView.as_view(), name='create_final_report'),
    path('teacher/report/final', FinalReportTeacherCreateView.as_view(), name='create_teacher_final_report'),    
    path('report/final/<int:pk>/', FinalReportPrintView.as_view(), name='final_report_print'), 
]
