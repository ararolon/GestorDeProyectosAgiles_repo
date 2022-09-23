from django.urls import path
from Sprint import views

"""
urls de la app de Sprint, vistas relacionadas a la creación de los sprints,
"""
urlpatterns = [
    path('crearSprint/', views.crearSprint, name='crearSprint'),
    path('mostrarSprint/', views.mostrarSprint, name='mostrarSprint'),
]
