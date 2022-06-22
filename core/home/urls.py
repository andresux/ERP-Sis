from django.urls import path
from core.home.views.home.views import HomeView

urlpatterns = [
    path('dashboard/', HomeView.as_view(), name='home'),
]