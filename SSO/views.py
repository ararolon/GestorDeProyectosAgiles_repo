
from multiprocessing import context
from unicodedata import name
from urllib import request
from django.shortcuts import render,redirect
from allauth.socialaccount.models import SocialApp


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from django.contrib import messages
from permisos.models import RolesdeSistema 
from UserStories.models import Estados_Kanban

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
       rol = RolesdeSistema.objects.create(nombre='administrador',defecto =True)
       rol.permisos.clear()
       grupo = Group.objects.create(name=rol.get_nombre())
       grupo.save()

   #pregunta por el grupo usuarios 

    if not Group.objects.filter(name='usuarios'):
       rol = RolesdeSistema.objects.create(nombre='usuarios',defecto=True)
       rol.permisos.clear()
       grupo = Group.objects.create(name='usuarios')
       grupo.save()
       perm= Permission.objects.get(codename='_acceder_al_sistema') 
       rol.permisos.add(perm)
       grupo.permissions.add(perm) # ya le asigna el permiso de acceder al sistema

   #pregunta por el grupo sin acceso

    if not Group.objects.filter(name='sin_acceso'):
        rol = RolesdeSistema.objects.create(nombre='sin_acceso', defecto=True)

        grupo = Group.objects.create(name='sin_acceso')
        grupo.save()

    if not RolesdeSistema.objects.filter(nombre='Scrum Master').exists():
        rol = RolesdeSistema.objects.create(nombre='Scrum Master', defecto=True)
        rol.permisos.clear()
        lista_de_permisos = [
            '_acceder_al_sistema',
            '_crear_roles',
            '_asignar_roles',
            '_visualizar_roles',
            '_eliminar_roles',
            '_crear_proyecto',
            '_editar_proyecto',
            '_visualizar_proyecto',
            '_cancelar_proyecto',
            '_eliminar_miembros',
            '_visualizar_historial_proyecto',
            '_modificar_fecha',
            '_modificar_estado_proyecto',
            '_crear_sprint',
            '_modificar_sprint',
            '_modificar_estado_sprint',
            '_crear_us',
            '_modificar_us',
            '_modificar_estado_us',
            '_cancelar_us',
            '_consultar_historial_us',
            '_modificar_backlog',
            '_modificar_sprint_backlog',
            '_crear_tipos_us',
            '_modificar_tipos_us',
            '_visualizar_kanban',
            '_iniciar_proyecto',
            '_asignar_us'
        ]
        rol.asignar_permisos(lista_de_permisos)
    
    #se crean los estados Kanban por defecto en el sistema
    if not Estados_Kanban.objects.filter(nombre='Pendiente').exists():
        estado = Estados_Kanban.objects.create(nombre='Pendiente',defecto=True)
        estado.save()
    if not Estados_Kanban.objects.filter(nombre='En curso').exists():
        estado = Estados_Kanban.objects.create(nombre='En curso',defecto=True)
        estado.save()
    if not Estados_Kanban.objects.filter(nombre='Finalizado').exists():
        estado = Estados_Kanban.objects.create(nombre='Finalizado',defecto=True, id=100)
        estado.save()


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
    Vista que redrecciona a la pagina principal del sistema dependiendo si el usuario es administrador del sistema o no

    :param request: HttpRequest object
    :return: HttpRedirect
    
    """
    #Pregunta si es el administrador del sistema o si es un usuario comun. 
    #Redirecciona a diferentes interfaces
    if request.user.groups.filter(name='administrador'):
        return render(request, 'SSO/home_admin.html', context=None)
    elif request.user.groups.filter(name='usuarios'):
        return render(request,'SSO/home_usuarios.html',context=None)
    else:   #los usuarios en el grupo 'sin acceso'
        return render(request,'SSO/sinpermiso.html',context=None)

@login_required(login_url='login')
def sin_permiso(request):
    """
    Vista para usuarios que no tienen permisos necesarios para visualizar una pantalla

    :param request: HttpRequest object
    :return: HttpRedirect

    """

    return render(request,'SSO/sinpermiso.html',context=None)
   




