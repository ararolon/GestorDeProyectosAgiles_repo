from sre_constants import GROUPREF_EXISTS
from tokenize import group
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission#importa el modelo de usuarios de Django para obtener todos los usuarios regigistrados en el sistema hasta ahora
from Usuarios.models import Usuario
"""
Vistas exclusivas del administrador del sistema sobre los usuarios

administrar usuarios del sistema
"""

def lista_eliminar(request):
    """
    Vista que permite ver todos los usuarios del sistema para luego borrarlos.
    :param request: Httprequest object
    :return: HttpResponse
    
    """

    lista = list(User.objects.filter(groups__name= 'usuarios'))
    return render(request,'Usuarios/index_eliminar.html',{'lista':lista})




@login_required(login_url='login')
def eliminar_usuario(request,id):
  
  """
    Vista que permite al administrador del sistema eliminar un usuario del sistema 

    :param request: HttpRequest object
    :param id: id del usuario a eliminar
    :return: HttpResponse o HttpRedirect

  """
    
  usuario = get_object_or_404(User,pk=id)

  if request.method =="POST":
      usuario.delete()
      return redirect('index_eliminar')
  else:
      return render(request,'Usuarios/eliminar.html',{'usuario':usuario})    


def listar_usuarios(request):
  
  """
   Vista que permite al administrador del sistema listar todos los usuarios del sistema 
   Si el usuario ya tiene permiso del sistema se deshabilita el boton de dar acceso pero
   si el usuario no tiene permiso, el boton esta disponible

    :param request: HttpRequest object
    :param id: id del usuario a eliminar
    :return: HttpResponse o HttpRedirect
  """
  
  usuarios = list(User.objects.filter(groups__name='usuarios'))

  return render(request,'Usuarios/listar_usuarios.html',{'usuarios':usuarios})
   

@login_required(login_url='login')
def crear_usuario(request,id):

  """
  Vista que permite al administrador del sistema dar permiso de acceder al sistema a otro usuario
 
  :param request: HttpRequest object
  :param id : id del usuario a eliminar

  """

  usuario =  get_object_or_404(User,pk=id)

  if request.method == 'POST':
    perm= Permission.objects.get(codename='acceder_al_sistema') 
    usuario.user_permissions.add(perm)
    return redirect('lista_users')

  else:
      return render(request,'Usuarios/Daracceso.html',{'usuario':usuario})    







