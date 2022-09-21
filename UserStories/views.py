from django.shortcuts import render, redirect, get_object_or_404
from .form import EstadosKanbanForm,TiposUSForm, UserStoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

"""
 vistas relacionadas a la app UserStories
"""
#@login_required(login_url='login')
#@permission_required('permisos._crear_tipos_us',login_url='sinpermiso')
def crear_estadokanban(request):
  
   """
    Vista que permite la creacion de un nuevo estado de kanban 

    Argumentos:
        request: HttpRequest
    Retorna:
        HttpResponse
   """
   contexto = {'user': request.user}
   contexto['form'] = EstadosKanbanForm()

   if request.method == 'POST':
        form = EstadosKanbanForm(request.POST)
        if form.is_valid():
            estado = form.save()
            estado.save()
            messages.success(request,"El estado "+estado.nombre+ " ha sido creado satisfactoriamente")
            #return redirect('listar_roles')
        else:
            contexto['mensajeError'] = 'El estado ya existe'
   else:
        contexto['form'] = EstadosKanbanForm()

   return render(request, 'UserStories/crear_estado.html',contexto)


#login_required(login_url='login')
#permission_required('permisos._crear_tipos_us',login_url='sinpermiso')
def crear_TipoUS(request):

    """
    Formulario para crear un nuevo tipo de US en el sistema
    
    Argumentos:
        request: HttpRequest
    Retorna:
        HttpResponse
    """

    contexto = {'user': request.user}
    contexto['form'] = TiposUSForm()

    if request.method == 'POST':
        form = TiposUSForm(request.POST)
        if form.is_valid():
            tipoUS = form.save()
            tipoUS.save()
            messages.success(request,"El Tipo de US "+tipoUS.nombre+" ha sido creado satisfactoriamente")
            #return redirect('listar_roles')
        else:
            contexto['mensajeError'] = 'El Tipo de US ya existe en el sistema'
    else:
        contexto['form'] = TiposUSForm()

    return render(request, 'UserStories/crear_tipoUS.html',contexto)

def crear_us(request):
    """
    Formulario para crear un nuevo tipo de US en el sistema
    
    Argumentos:
        request: HttpRequest
    Retorna:
        HttpResponse
    """

    contexto = {'user': request.user}
    contexto['form'] = UserStoryForm()

    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            us = form.save()
            us.save()
            messages.success(request,"El User Story "+us.nombre+" ha sido creado satisfactoriamente")
            #return redirect('listar_roles')
        else:
            contexto['mensajeError'] = 'El User Story no pude crearse correctamente'
    else:
        contexto['form'] = UserStoryForm()

    return render(request, 'UserStories/crear_US.html',contexto)

