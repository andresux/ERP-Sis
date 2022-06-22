from django.urls import path
from .views.audit.views import *

urlpatterns = [
    path('audit/', AuditListView.as_view(), name='audit_list'),
    path('audit/delete/<int:pk>/', AuditDeleteView.as_view(), name='audit_delete'),
]
