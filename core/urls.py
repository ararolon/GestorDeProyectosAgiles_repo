
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include

"""
 urls del proyecto
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('SSO.urls')),
    path('',include('permisos.urls')),
    path('accounts/',include('allauth.urls')), #path del sso
]
