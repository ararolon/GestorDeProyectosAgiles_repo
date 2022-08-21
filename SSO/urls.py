"""
    urls de la app de SSO de Google , vistas de paginas principales
    login y logout del proyecto
"""

import imp
from django.urls import path, include

from SSO import views

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('',views.configurar_sso,name='configurar_sso'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]