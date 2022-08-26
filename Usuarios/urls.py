
from xml.etree.ElementInclude import include
from django.urls import path,include
from Usuarios import views


urlpatterns = [
    path('eliminarUser/<int:id>',views.eliminar_usuario,name='eliminar_user'), #path de las urls de Usuarios
    path('index_usuario/',views.lista_eliminar,name='index_eliminar'),
]
