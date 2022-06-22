from django.urls import path, re_path
from core.login.views.login.views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('distinct/session/', LoginView.as_view(), name='login_distinct_session'),
    path('change/password/<str:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('authenticated/', LoginAuthenticatedView.as_view(), name='login_authenticated'),
]