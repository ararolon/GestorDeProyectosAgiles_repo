from django.shortcuts import render, redirect,reverse, get_object_or_404
from Sprint.forms import crearSprintForm
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages

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
            return redirect('home')
    else:
         form = crearSprintForm()
    contexto = {'form': form
                }
    return render(request,'Sprint/crearSprint.html',context=contexto)    
