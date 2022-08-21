"""
    urls de la app de SSO de Google , vistas de paginas principales
    login y logout del proyecto
"""

import imp
from django.urls import path, include

from SSO import views

urlpatterns = [
     path('configuracion_inicial/',views.configuraciones_iniciales,name='confinicial'),
    path('index/', views.index, name='index'), 
    path('',views.configurar_sso,name='configurar_sso'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]