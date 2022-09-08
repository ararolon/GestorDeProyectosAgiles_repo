
from django.urls import path

from Proyectos import views

urlpatterns = [
    path('crearProyecto/', views.crearProyecto, name='crearProyecto'), 
]