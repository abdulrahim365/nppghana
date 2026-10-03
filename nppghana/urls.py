"""
URL configuration for nppghana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

admin.site.site_header = "NPP Ghana Administration"
admin.site.site_title = "NPP Admin"
admin.site.index_title = "Dashboard"
from core.views import (
    home, about, leadership, achievements, contact,
    history, manifesto, constituencies,  privacy, terms,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('leadership/', leadership, name='leadership'),
    path('achievements/', achievements, name='achievements'),
    path('contact/', contact, name='contact'),
    path('history/', history, name='history'),
    path('manifesto/', manifesto, name='manifesto'),
    path('constituencies/', constituencies, name='constituencies'),
    path('members/', include('members.urls')),
    path('news/', include('blog.urls')),
    path("privacy/", privacy, name="privacy"),
    path("terms/", terms, name="terms"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)