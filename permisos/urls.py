"""
    urls de la app de SSO de Google , vistas de paginas principales
    login y logout del proyecto
"""


from django.urls import path, include

from . import views

urlpatterns = [
    path('crearRol/', views.crear_rol, name='crear_rol'), 
    path('listarRol/', views.listar_roles, name='listar_roles'), 
    path('<int:id_rol>/modificarRol', views.modificar_rol, name='modificar_rol'),
    path('<int:id_rol>/eliminarRol', views.eliminar_rol, name='eliminar_rol'),
]