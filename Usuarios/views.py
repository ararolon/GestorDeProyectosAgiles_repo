from email.headerregistry import Group
from sre_constants import GROUPREF_EXISTS
from tokenize import group
from unicodedata import name
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User,Group, Permission
from Usuarios.forms import AsignarRolForm
from Usuarios.models import Usuario,Notificaciones
from django.contrib import messages
"""
Vistas exclusivas del administrador del sistema sobre los usuarios

administrar usuarios del sistema
"""

def lista_eliminar(request):
    """
    Vista que permite ver todos los usuarios del sistema para luego borrarlos.
    Lista de usuarios con acceso y sin acceso al sistema.
    :param request: Httprequest object
    :return: HttpResponse
    
    """

    lista = list(User.objects.filter(groups__name= 'usuarios'))
    lista = lista + list(User.objects.filter(groups__name='sin_acceso'))
    return render(request,'Usuarios/index_eliminar.html',{'lista':lista})





def eliminar_usuario(request,id):
  
  """
    Vista que permite al administrador del sistema eliminar un usuario del sistema 

    :param request: HttpRequest object
    :param id: id del usuario a eliminar
    :return: HttpResponse o HttpRedirect

  """
    
  usuario = get_object_or_404(Usuario,pk=id)
  
  if request.method =="POST":
    if usuario.miembro_en_uso() == False :
      usuario.delete()
      messages.success(request,"El usuario ha sido eliminado")
      return redirect('index_eliminar')
    else:
        messages.error(request,"El usuario no puede eliminarse , es parte de un proyecto en el sistema")
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
  
  usuarios = list(User.objects.filter(groups__name='sin_acceso'))
  usuarios = usuarios + list(User.objects.filter(groups__name='usuarios'))

  return render(request,'Usuarios/listar_usuarios.html',{'usuarios':usuarios})
   


def crear_usuario(request,id):

  """
  Vista que permite al administrador del sistema dar permiso de acceder al sistema a otro usuario
  Le asigna al grupo 'rol' que tienen el permiso de acceder al sistema (usuarios)

  :param request: HttpRequest object
  :param id : id del usuario a eliminar

  """
  usuario =  get_object_or_404(User,pk=id)

  if request.method == 'POST':
      #elimina el rol de 'sin acceso'
      usuario.groups.clear()
      acceso =  Group.objects.get(name='usuarios')
      usuario.groups.add(acceso)
      messages.success(request,"Se ha otorgado permiso de acceso al usuario "+usuario.username)
      return redirect('lista_users')

  else:
      return render(request,'Usuarios/Daracceso.html',{'usuario':usuario})    
  

def asignar_rol_usuario(request,id):
 
  """
  Vista que permite asignar un rol a un usuario
  :param request: HttpRequest object
  :param id : id del usuario al que se le quiere aignar un rol.
  """

  usuario = get_object_or_404(Usuario,pk=id) #se busca el usuario por id
 
  if request.method == 'POST':
    form = AsignarRolForm (request.POST, usuario=usuario)
    if form.is_valid():
      usuario.asignar_roles_usuarios(form.cleaned_data.get('Roles')) #obtiene los roles seleccionado
      return redirect('lista_users')  
    
  else:
    form = AsignarRolForm(usuario=usuario)

  contexto = {'usuario':usuario, 'user':request.user, 'form':form}

  return render(request,'Usuarios/asignar_rol.html',contexto)


def ver_notificaciones(request,username):
  """
   Vista que permite ver obtener todas las notificaciones de un usuario
   y mostrar en la barra de navegacion 
  
  Argumentos:
    request : HttpRequest object
    username : El username del usuario con el cual se filtraran las notificaciones
  
  Retorna:
      JsonResponse 
  """
  print(username)
  user =  Usuario.objects.get(username=username)
  print(user)
  notificaciones = Notificaciones.objects.filter(usuario=user)
  
  data = list(notificaciones.values())
  return JsonResponse(data, safe=False)


def listar_notificaciones(request,username):
  """
   Vista que permite ver todas las notificaciones de un usuario 

   Argumento:
        request : HttpRequest object
        username : El username del usuario con el cual se filtraran las notificaciones
    
    Return
        HttpResponse
  """

  user =  get_object_or_404(Usuario,username=username)
  notificaciones = Notificaciones.objects.filter(usuario=user).order_by('-timestamp')
  contexto = {'notificaciones':notificaciones}

  return render(request,'Usuarios/notificaciones.html',contexto)


  
   

