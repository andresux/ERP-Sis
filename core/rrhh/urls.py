from django.urls import path
from core.rrhh.views.job.views import *
from core.rrhh.views.elements_rol.views import *
from core.rrhh.views.contracts.views import *
from core.rrhh.views.assistance.views import *
from core.rrhh.views.salary.views import *
from core.rrhh.views.events.views import *

urlpatterns = [
    # job
    path('job/', JobListView.as_view(), name='job_list'),
    path('job/add/', JobCreateView.as_view(), name='job_create'),
    path('job/update/<int:pk>/', JobUpdateView.as_view(), name='job_update'),
    path('job/delete/<int:pk>/', JobDeleteView.as_view(), name='job_delete'),
    # elements_rol
    path('elements/rol/', ElementsRolListView.as_view(), name='elements_rol_list'),
    path('elements/rol/add/', ElementsRolCreateView.as_view(), name='elements_rol_create'),
    path('elements/rol/update/<int:pk>/', ElementsRolUpdateView.as_view(), name='elements_rol_update'),
    path('elements/rol/delete/<int:pk>/', ElementsRolDeleteView.as_view(), name='elements_rol_delete'),
    # contracts
    path('contracts/', ContractsListView.as_view(), name='contracts_list'),
    path('contracts/add/', ContractsCreateView.as_view(), name='contracts_create'),
    path('contracts/update/<int:pk>/', ContractsUpdateView.as_view(), name='contracts_update'),
    path('contracts/delete/<int:pk>/', ContractsDeleteView.as_view(), name='contracts_delete'),
    # assistance
    path('assistance/', AssistanceListView.as_view(), name='assistance_list'),
    path('assistance/add/', AssistanceCreateView.as_view(), name='assistance_create'),
    path('assistance/update/<int:pk>/', AssistanceUpdateView.as_view(), name='assistance_update'),
    path('assistance/delete/<int:pk>/', AssistanceDeleteView.as_view(), name='assistance_delete'),
    path('assistance/insert/', InsertAssistanceView.as_view(), name='assistance_insert'),
    # salary
    path('salary/', SalaryListView.as_view(), name='salary_list'),
    path('salary/add/', SalaryCreateView.as_view(), name='salary_create'),
    path('salary/delete/<int:year>/<int:month>/', SalaryDeleteView.as_view(), name='salary_delete'),
    # Events
    path('events/', EventsListView.as_view(), name='events_list'),
    path('events/add/', EventsCreateView.as_view(), name='events_create'),
    path('events/update/<int:pk>/', EventsUpdateView.as_view(), name='events_update'),
    path('events/delete/<int:pk>/', EventsDeleteView.as_view(), name='events_delete'),
]
