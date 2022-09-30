
"""
    urls de la app de Ptoyectos , vistas de las páginas para crear proyecto,
    visualizar proyectos y visualizar proyectos individuales de un usuario
"""

from django.urls import path

from Proyectos import views

urlpatterns = [
    path('crearProyecto/', views.crearProyecto, name='crearProyecto'), 
    path('listarProyectos/', views.listarProyectos, name='listarProyectos'), 
    path('listarProyectosUser/', views.listarProyectosUser, name='listarProyectosUser'), 
    path('asignar_miembro/<int:id_proyecto>', views.asignar_miembro, name='asignar_miembro'),
    path('mostrarProyecto/<int:id_proyecto>', views.mostrarProyecto, name='mostrarProyecto'),
    path('mostrarProyectoAdmin/<int:id_proyecto>', views.mostrarProyectoAdmin, name='mostrarProyectoAdmin'),
    path('importarRol/<int:id_proyecto>', views.importarRol, name='importarRol'),
    path('asignarRol/<int:id_proyecto>/miembro/<int:id_usuario>', views.asignarRol, name='asignarRol'),
    path('iniciarProyecto/<int:id_proyecto>', views.iniciarProyecto, name='iniciarProyecto'),
    path('cancelarProyecto/<int:id_proyecto>', views.cancelarProyecto, name='cancelarProyecto'),
    

]