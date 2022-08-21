from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import request
from django.shortcuts import render, redirect


# Create your views here.
#from vistasSSO.decorator import agregar_usuarios

def home(request):
    """
    vista home del Sistema
    """
    return render(request, 'vistasSSO/home.html', context=None)



#def login(request):
    """
    Vista que dirige al SSO de google
    :para request: HttpRequest object
    :return: HttpRedirect
    """
 #   return redirect('/accounts/google/login/?process=login')




"""
vista para log out del Sistema
"""
def logout(request):
    """
     Ir a la pagina de cierre de sesion de google
    :param request: HttpRequest object
    :return:HttpRedirect
    """
    return redirect('/accounts/logout/')

#@login_required(login_url='login')
#def home(request):
    """
    Vista principal cuando se conecta un usuario
    :param:
        request (HttpRequest Object): respuesta del request
    :return
        El HttpResponse de la vista a mostrarse
    """

    #pregunta si el usuario es el administrador
    #if request.user.groups.filter(name='administrador'):
    #    return render(request, 'vistasSSO/home.html', context=None)
    #elif request.user.groups.filter(name='usuarios'):
     #   return render(request,'vistasSSO/Home_usuario.html',context=None)
   # else:
   #     return redirect('login')



def configuraciones_iniciales(request):

   """
    Se realizan las configuraciones iniciales para la identificacion de usuarios.
    Se crea un grupo administrador y de usuarios si es que todavia no existe en
    el sistema.
   :param request: HttpREquest object
   :return: HttpRedirect
   """
   #verificar si es del grupo Administrador
   if not Group.objects.filter(name='administrador').exists():
       grupo = Group.objects.create(name='administrador')
       grupo.save()

   #verificar si es del grupo de Usuarios 

   if not Group.objects.filter(name='usuarios'):
       grupo = Group.objects.create(name='usuarios')
       grupo.save()

   return redirect('home')

