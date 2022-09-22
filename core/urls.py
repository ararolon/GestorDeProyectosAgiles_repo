
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include

"""
 urls de la app Usuarios
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('SSO.urls')),
    path('',include('permisos.urls')),
    path('accounts/',include('allauth.urls')), #path del sso
    path('',include('Proyectos.urls')),
    path('usuarios/',include('Usuarios.urls')),#path de usuarios
    path('userstories/',include('UserStories.urls')),
    path('',include('Sprint.urls')),
]
