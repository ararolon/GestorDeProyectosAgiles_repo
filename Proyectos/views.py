from urllib import request
from django.shortcuts import render, redirect,reverse
from Proyectos.forms import crearproyectoForm
from Proyectos.models import Proyecto
from django.utils import timezone
from django.forms import model_to_dict
# Create your views here.



def crearProyecto (request):
    """
    Metodo para proyecto nuevo a crear
    param request: request para datos nuevos de un proyecto
    return: contexto para proyecto nuevo
    """


    if request.method == 'POST':
        form = crearproyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.fecha_de_inicio = timezone.now()
            proyecto.save()
            return redirect('home')
    else:
         form = crearproyectoForm()
    contexto = {'form': form
                }
    return render(request,'proyectos/crearProyectos.html',context=contexto)    


   