from urllib import request
from django.shortcuts import render, redirect,reverse, get_object_or_404
from Proyectos.forms import AsignarMiembroForm, crearproyectoForm
from Proyectos.models import Proyecto
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages
# Create your views here.



def crearProyecto (request):
    """
    Metodo para crear proyecto
    param request: request para datos nuevos de un proyecto
    return: contexto para proyecto nuevo
    """


    if request.method == 'POST':
        form = crearproyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.fecha_de_inicio = timezone.now()
            proyecto.save()
            messages.success(request,"Se ha creado el proyecto satisfactoriamente")
            return redirect('home')
    else:
         form = crearproyectoForm()
    contexto = {'form': form
                }
    return render(request,'proyectos/crearProyectos.html',context=contexto)    


def listarProyectos(request):
    """
    Vista que muestra al usuario la lista de Proyectos que existen dentro del Sistema.
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    # los proyectos aceptados son los que el usuario:
    # 1 es scrum master o
    # 2 miembro
    proyectos = Proyecto.objects.all()
    contexto = {
        'proyectos': [
            {
                'id': Proyecto.id,
                'nombre': Proyecto.nombre,
                'descripcion': Proyecto.descripcion,
                'scrumMaster': Proyecto.scrumMaster,
            } for Proyecto in proyectos
        ],
    }
    return render(request, 'proyectos/listarProyectos.html', contexto)

def listarProyectosUser(request):
    """
    Vista que muestra al usuario la lista de Proyectos que existen dentro del Sistema.
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    # los proyectos aceptados son los que el usuario:
    # 1 es scrum master o
    # 2 miembro
    proyectos = (
        Proyecto.objects.filter(miembros__id=request.user.id) 
        | Proyecto.objects.filter(scrumMaster=request.user.id)
    ).distinct() # para que no se repitan los proyectos

    contexto = {
        'proyectos': [
            {
                'id': Proyecto.id,
                'nombre': Proyecto.nombre,
                'descripcion': Proyecto.descripcion,
                'scrumMaster': Proyecto.scrumMaster,
            } for Proyecto in proyectos
        ],
    }
    return render(request, 'proyectos/listarProyectosUser.html', contexto)

def mostrarProyecto(request, id_proyecto):
    """
    Vista que donde el Scrum master puede seleccionar los participantes del proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    print('*'*66)
    print(id_proyecto)
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    form = AsignarMiembroForm(instance=proyecto)
    if request.method == 'POST':
        form = AsignarMiembroForm( instance=proyecto, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los miembros han sido asignado al proyecto')
            return redirect('home')
    contexto = {
        'form': form,
        'proyecto': proyecto,
    }
    return render(request, 'proyectos/mostrarProyecto.html', contexto)

def asignar_miembro(request, id_proyecto):
    """
    Vista que donde el Scrum master puede seleccionar los participantes del proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    print('*'*66)
    print(id_proyecto)
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    form = AsignarMiembroForm(instance=proyecto)
    if request.method == 'POST':
        form = AsignarMiembroForm( instance=proyecto, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los miembros han sido asignado al proyecto')
            return redirect('home')
    contexto = {
        'form': form,
        'proyecto': proyecto,
    }
    return render(request, 'proyectos/asignar_miembro.html', contexto)