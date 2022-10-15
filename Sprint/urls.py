from django.urls import path
from Sprint import views

"""
urls de la app de Sprint, vistas relacionadas a la creación de los sprints,
"""
urlpatterns = [
    path('crearSprint/<int:id>', views.crearSprint, name='crearSprint'),
    path('iniciarSprint/<int:id_sprint>', views.iniciarSprint, name='iniciarSprint'),
    path('cancelarSprint/<int:id_sprint>', views.cancelarSprint, name='cancelarSprint'),
    path('listarSprint/<int:id>', views.listarSprint, name='listarSprint'),
    path('AsignarUS/<int:id_sprint>',views.asignar_us,name='asignarUS'),
    path('modificarSprint/<int:id>/<int:id_sprint>', views.modificarSprint, name='modificarSprint'),
    path('asignarMiembroSprint/<int:id_sprint>', views.asignarMiembroSprint, name='asignarMiembroSprint'),
    path('asignar_us_miembro/<int:id_sprint_miembro>', views.asignarUSMiembro, name='asignar_us_miembro'),    
]
