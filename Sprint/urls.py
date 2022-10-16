from django.urls import path
from Sprint import views

"""
urls de la app de Sprint, vistas relacionadas a la creación de los sprints,
"""
urlpatterns = [
    path('crearSprint/<int:id>', views.crearSprint, name='crearSprint'),
    path('mostrarSprint/', views.mostrarSprint, name='mostrarSprint'),
    path('sprint_miembros/<int:id_sprint>', views.sprint_miembros, name='sprint_miembros'),
    path('iniciarSprint/<int:id_sprint>', views.iniciarSprint, name='iniciarSprint'),
    path('cancelarSprint/<int:id_sprint>', views.cancelarSprint, name='cancelarSprint'),
    path('listarSprint/<int:id>', views.listarSprint, name='listarSprint'),
    path('AsignarUS/<int:id_sprint>',views.asignar_us,name='asignarUS'),
    path('SprintBacklog/<int:id>',views.ver_sprintbacklog,name='sprintbacklog'),
]


