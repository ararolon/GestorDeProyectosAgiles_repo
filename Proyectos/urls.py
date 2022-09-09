
"""
    urls de la app de Ptoyectos , vistas de las páginas para crear proyecto,
    visualizar proyectos y visualizar proyectos individuales de un usuario
"""

from django.urls import path

from Proyectos import views

urlpatterns = [
    path('crearProyecto/', views.crearProyecto, name='crearProyecto'), 
    path('listarProyectos/', views.listarProyectos, name='listarProyectos'), 
    path('mostrarUnProyecto/', views.mostrarUnProyecto, name='mostrarUnProyecto'), 
]