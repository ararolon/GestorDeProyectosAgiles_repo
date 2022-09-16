from django.shortcuts import render, redirect, get_object_or_404
from .form import EstadosKanbanForm,TiposUSForm
from django.contrib import messages
# Create your views here.

"""
 vistas relacionadas a la app UserStories
"""

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



