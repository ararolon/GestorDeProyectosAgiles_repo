"""
 urls de la app de UserStories, vistas relacionadas a los tipos de user stories,
 user stories y estados del kanban relacionado a un tipo de user story.
"""

from unicodedata import name
from django.urls import path, include

from . import views

urlpatterns = [
    path('crearEstado/<int:id>',views.crear_estadokanban,name='crear_estado'),
    path('crearTipoUS/<int:id>',views.crear_TipoUS,name='crear_tipoUS'),
    path('crearUS/<int:id>',views.crear_us,name='crear_us'),
    path('importarTipoUS/<int:id>',views.importar_tipoUS,name='importar_tipoUS'),
    path('productBacklog/<int:id>',views.ver_product_backlog,name='product_backlog'),
    path('listarTipoUS/<int:id>',views.listarTipoUS,name='listarTipoUS'),
    path('tabla_kanban/<int:id_proyecto>',views.tablaKanban,name='tabla_kanban'),
    path('cambiarEstado/<int:id_us>/estado/<int:id_estado>',views.cambiarEstado,name='cambiarEstado'),
    path('modificarTipoUS/<int:id>/<int:id_tipo>/',views.modificar_tipoUS,name='modificar_tiposUS'),
    path('eliminarTiposUS/<int:id>/<int:id_tipo>/',views.eliminar_tipoUS,name='eliminar_tipoUS'),
    path('modificarUS/<int:id_proyecto>/<int:id>/',views.modificarUS,name='modificar_us'),
    path('cancelarUS/<int:id>/',views.cancelar_US,name='cancelarUS'),
    path('cargarHoras/',views.cargarHoras,name='cargarHoras'),

]