from django.urls import path
from .views.comments_report.views import *
from .views.student_report.views import *
from .views.contracts_report.views import *
from .views.assistance_report.views import *
from .views.person_report.views import *
from .views.ctas_pay_report.views import *
from .views.salary_report.views import *
from .views.payments_report.views import *
from .views.ingress_report.views import *

urlpatterns = [
    path('comments/report/', CommentsReportView.as_view(), name='comments_report'),
    path('student/report/', StudentReportView.as_view(), name='student_report'),
    path('contracts/report/', ContractsReportView.as_view(), name='contracts_report'),
    path('assistance/report/', AssistanceReportView.as_view(), name='assistance_report'),
    path('person/report/', PersonReportView.as_view(), name='person_report'),
    path('ctas/pay/report/', CtasPayReportView.as_view(), name='ctas_pay_report'),
    path('salary/report/', SalaryReportView.as_view(), name='salary_report'),
    path('payments/report/', PaymentsReportView.as_view(), name='payments_report'),
    path('ingress/report/', IngressReportView.as_view(), name='ingress_report'),
]
