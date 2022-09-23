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

def mostrarSprint (request):
    """
    Metodo para mostrar sprint
    """
    sprint = Sprint.objects.all()
    contexto = {
        'sprint': [
            {
                'id': Sprint.id_sprint,
                'nombre': Sprint.nombre_sprint,
                'descripcion': Sprint.descripcion,
            } for Sprint in sprint
        ],
    }
    return render(request, 'Sprint/mostrarSprint.html', contexto)
