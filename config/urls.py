"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import settings as setting
from core.home.views.home.views import *

urlpatterns = [
    path('', include('core.homepage.urls')),
    path('home/', include('core.home.urls')),
    path('admin/', admin.site.urls),
    path('security/', include('core.security.urls')),
    path('login/', include('core.login.urls')),
    path('user/', include('core.user.urls')),
    path('college/', include('core.college.urls')),
    path('ingress/', include('core.ingress.urls')),
    path('rrhh/', include('core.rrhh.urls')),
    path('reports/', include('core.reports.urls')),
]

# handler400 = error_404
# handler500 = error_500

if setting.DEBUG:
    urlpatterns += static(setting.STATIC_URL, document_root=setting.STATIC_ROOT)
    urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)
