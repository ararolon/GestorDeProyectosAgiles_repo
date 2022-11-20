from django.urls import path
from Sprint import views

"""
urls de la app de Sprint, vistas relacionadas a la creación de los sprints,
"""
urlpatterns = [
    path('crearSprint/<int:id>', views.crearSprint, name='crearSprint'),
    path('iniciarSprint/<int:id_sprint>', views.iniciarSprint, name='iniciarSprint'),
    path('cancelarSprint', views.cancelarSprint, name='cancelarSprint'),
    path('finalizarSprint', views.finalizarSprint, name='finalizarSprint'),
    path('listarSprint/<int:id>', views.listarSprint, name='listarSprint'),
    path('IndexAsignar/<int:id_sprint>',views.index_asignar,name='indexasignar'),
    path('AsignarUS/<str:nombre>/<int:id_sprint>',views.asignar_us,name='asignarUS'),
    path('modificarSprint/<int:id>/<int:id_sprint>', views.modificarSprint, name='modificarSprint'),
    path('asignarMiembroSprint/<int:id_sprint>', views.asignarMiembroSprint, name='asignarMiembroSprint'),
    path('SprintBacklog/<int:id>',views.ver_sprintbacklog,name='sprintbacklog'),
    path('QuitarUS/<str:nombre>/<int:id_sprint>',views.desasignar_us,name='desasignar'),
    path('asignarHistoria/<int:id_sprint>', views.asignarHistoria, name="asignarHistoria"),
    path('burnDownChart/<int:id>',views.burnDownChart,name='burnDownChart'),

]


