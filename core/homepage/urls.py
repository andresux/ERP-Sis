from django.urls import path
from .views.homepage.views import *

urlpatterns = [
    path('', HomepageView.as_view(), name='index'),
]