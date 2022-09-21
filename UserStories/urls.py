"""
 urls de la app de UserStories, vistas relacionadas a los tipos de user stories,
 user stories y estados del kanban relacionado a un tipo de user story.
"""

from unicodedata import name
from django.urls import path, include

from . import views

urlpatterns = [
    path('crearEstado/',views.crear_estadokanban,name='crear_estado'),
    path('crearTipoUS/',views.crear_TipoUS,name='crear_tipoUS'),
    path('crearUS/',views.crear_us,name='crear_us'),
]