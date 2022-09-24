from django.shortcuts import render, redirect,reverse, get_object_or_404
from Sprint.forms import crearSprintForm
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages
from Sprint.models import Sprint

# Create your views here.


def crearSprint (request):
    """
    Metodo para crear sprint
    param request: request para datos nuevos de un sprint
    return: contexto para sprint nuevo
    """

    if request.method == 'POST':
        form = crearSprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.fecha_de_inicio = timezone.now()
            sprint.fecha_de_fin = timezone.now()
            sprint.save()
            messages.success(request,"Se ha creado el sprint satisfactoriamente")
            return redirect('mostrarSprint')
    else:
         form = crearSprintForm()
    contexto = {'form': form
                }
    return render(request,'Sprint/crearSprint.html',context=contexto)    


def mostrarSprint(request):
    """
    Metodo para mostrar sprint.
    Argumentos:
        request: HttpRequest
    Retorna:
        HttpResponse
    """
    contexto = {
        'sprints': [
            {
                'id_sprint': sprint.id_sprint, 
                'nombre_sprint': sprint.nombre_sprint, 
                'fecha_inicio': sprint.fecha_inicio,
                'fecha_fin': sprint.fecha_fin,
                'descripcion': sprint.descripcion,
            }
            for sprint in Sprint.objects.all()
        ],
    }

    return render(request, 'Sprint/mostrarSprint.html', contexto)


def iniciarSprint(request, id_sprint):
    """
    Vista donde el Scrum master puede iniciar un sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    sprint = get_object_or_404(Sprint, id=id_sprint)
    sprint.estado_sprint = 'En Curso'
    sprint.save()
    return redirect('Sprint/mostrarSprint.html', id_sprint=id_sprint)


def cancelarSprint(request, id_sprint):
    """
    Vista donde el Scrum master puede cancelar un proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    sprint = get_object_or_404(Sprint, id=id_sprint)
    sprint.estado_sprint = 'Cancelado'
    sprint.save()
    return redirect('mostrarSprint', id_sprint=id_sprint)
