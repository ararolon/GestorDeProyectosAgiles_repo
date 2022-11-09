
from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import path,include
from Usuarios import views


urlpatterns = [
    path('eliminarUser/<int:id>',views.eliminar_usuario,name='eliminar_user'), #path de las urls de Usuarios
    path('index_usuario/',views.lista_eliminar,name='index_eliminar'),
    path('listar_usuarios/',views.listar_usuarios,name='lista_users'),
    path('dar_acceso/<int:id>',views.crear_usuario,name='dar_acceso'),
    path('asignarRol/<int:id>',views.asignar_rol_usuario,name='asignar_rol'),
    path('notificaciones/<str:username>',views.ver_notificaciones,name='notificaciones')
] 
