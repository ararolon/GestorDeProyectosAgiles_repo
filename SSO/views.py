
from unicodedata import name
from urllib import request
from django.shortcuts import render,redirect
from allauth.socialaccount.models import SocialApp


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.urls import reverse

from . import decoradores

from .forms import SocialAppForm

"""
Vistas de configuraciones iniciales del SSO, login , logout 
"""


def configurar_sso(request):

    """
       Se realizan las configuraciones iniciales para la identificacion de usuarios.
       Se crea un grupo administrador y de usuarios si es que todavia no existe en
       el sistema.
       Se configuran los campos CLIEND_ID y el SECRET_KEY del Single Sign On.
       :param request: HttpREquest object
       :return: HttpRedirect
    """
   
    if  SocialApp.objects.filter(provider='google').exists():  
        return redirect('home')
    
    if not Group.objects.filter(name='administrador').exists():
       grupo = Group.objects.create(name='administrador')
       grupo.save()

   #pregunta por el grupo usuarios

    if not Group.objects.filter(name='usuarios'):
       grupo = Group.objects.create(name='usuarios')
       grupo.save()

    sa = SocialApp.objects.create(name="sso")
    sa.save()
    form = SocialAppForm(request.POST or None, instance=sa)
       
    if request.method == 'POST':
       if form.is_valid():
            form.save()
            
            return redirect('home')    
        
    contexto = {'form':form}
    return render(request,'SSO/configurar.html',context=contexto)    
    

def login(request):
    """
    Vista que redirecciona al SSO de google, primero verifica que el SSO este configurado
    :param request: HttpRequest object
    :return: HttpRedirect
    """
    if  not SocialApp.objects.filter(provider='google').exists():  
        return redirect('configurar_sso')     

    return redirect('/accounts/google/login/?process=login')

def logout(request):
    """
    Redirecciona a la pagina de cerrar sesion de google
    :param request: HttpRequest object
    :return:HttpRedirect
    """
    return redirect('/accounts/logout/')


@login_required(login_url='login')
@decoradores.agregar_usuarios
def home(request):
    """
     Vista de prueba para ver el indice de la pagina luego del login de un usuario
    
    :param request: HttpRequest object
    :return: HttpRedirect
    
    """
    #Pregunta si es el administrador del sistema o si es un usuario comun. 
    #Redirecciona a diferentes interfaces

    if request.user.groups.filter(name='administrador'):
        return render(request, 'SSO/home.html', context=None)
    elif request.user.groups.filter(name='usuarios'):
        return render(request,'SSO/sinpermiso.html',context=None)
    else:
        return redirect('login')

    return render(request,'SSO/home.html',context=None)
    


   




