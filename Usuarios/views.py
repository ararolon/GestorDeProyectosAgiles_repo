from sre_constants import GROUPREF_EXISTS
from tokenize import group
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User #importa el modelo de usuarios de Django para obtener todos los usuarios regigistrados en el sistema hasta ahora
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

  






