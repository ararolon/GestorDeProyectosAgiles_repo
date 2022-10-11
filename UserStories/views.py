from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404

from UserStories.models import Estados_Kanban, TipoUSerStory, UserStories
from .form import EstadosKanbanForm,TiposUSForm, UserStoryForm,ImportarTipoUSForm
from django.contrib import messages
from Proyectos.models import Proyecto
# Create your views here.

"""
 vistas relacionadas a la app UserStories
"""

def crear_estadokanban(request,id):
  
   """
    Vista que permite la creacion de un nuevo estado de kanban 

    Argumentos:
        request: HttpRequest
        id : id del proyecto
    Retorna:
        HttpResponse
   """
   proyecto = get_object_or_404(Proyecto,id=id)
   contexto = {'user': request.user,'proyecto':proyecto}
   contexto['form'] = EstadosKanbanForm()

   if request.method == 'POST':
        form = EstadosKanbanForm(request.POST)
        if form.is_valid():
            estado = form.save()
            estado.save()
            messages.success(request,"El estado "+estado.nombre+ " ha sido creado satisfactoriamente")
            return redirect('crear_tipoUS',id=id)
        else:
            contexto['mensajeError'] = 'El estado ya existe'
   else:
        contexto['form'] = EstadosKanbanForm()

   return render(request, 'UserStories/crear_estado.html',contexto)


def crear_TipoUS(request,id):

    """
    Formulario para crear un nuevo tipo de US en el sistema
    
    Argumentos:
        request: HttpRequest
        id : id del proyecto
    Retorna:
        HttpResponse
    """
    proyecto = get_object_or_404(Proyecto,id=id)
    form = TiposUSForm()
    contexto = {'form': form,'proyecto':proyecto}


    if request.method == 'POST':
        form = TiposUSForm(request.POST)
        if form.is_valid():
            tipoUS = form.save()
            tipoUS.save()
            messages.success(request,"El Tipo de US "+tipoUS.nombre+" ha sido creado satisfactoriamente")
            return render(request, 'proyectos/mostrarProyecto.html',contexto)
        else:
            messages.error(request,'El Tipo de User Story no pudo crearse, ya existe en el sistema')

    return render(request, 'UserStories/crear_tipoUS.html',contexto)

def crear_us(request,id):
    """
    Formulario para crear un nuevo tipo de US en el sistema
    
    Argumentos:
        request: HttpRequest
         id : id del proyecto
    Retorna:
        HttpResponse
    """
    proyecto = get_object_or_404(Proyecto,id=id)
    contexto = {'user': request.user,'proyecto':proyecto}
    contexto['form'] = UserStoryForm(proyecto)
   

    if request.method == 'POST':
        form = UserStoryForm(proyecto, data=request.POST)
        if form.is_valid():
            us = form.cleaned_data['nombre']
            us = form.save()
            us.id_proyecto = proyecto.id
            us.estado = us.tipo.estados_kanban.all().first()
            us.save()
            messages.success(request,"El User Story "+us.nombre+" ha sido creado satisfactoriamente")
            return render(request, 'proyectos/mostrarProyecto.html', {'proyecto':proyecto})
                
        else:
            messages.error(request,"El tipo de US no pudo ser creado, ya existe en el sistema")
    else:
        contexto['form'] = UserStoryForm(proyecto)
   

    return render(request, 'UserStories/crear_US.html',contexto)


def importar_tipoUS(request,id):
   
    """
      Llama al formulario para importar tipos de user stories a un proyecto
        
        Argumentos:
          request: HttpRequest
          id : id del proyecto
        Retorna:
          HttpResponse
    """
    proyecto = get_object_or_404(Proyecto,id=id)
    tipos =  TipoUSerStory.objects.all()
    contexto = {'user': request.user,'proyecto':proyecto,'tipos':tipos}
    contexto['form'] = ImportarTipoUSForm(proyecto,instance=proyecto)

    if request.method == 'POST':
        form = ImportarTipoUSForm(proyecto,instance=proyecto,data=request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo_us']
            proyecto.tipo_us.set(tipo)
            proyecto.save()
            messages.success(request,"Los tipos de User Stories han sido importados satisfactoriamente")
            return render(request, 'proyectos/mostrarProyecto.html', {'proyecto':proyecto})
        else:
            contexto['mensajeError'] = 'No se han podido importar los tipos de User Stories'
    else:
        contexto['form'] = ImportarTipoUSForm(proyecto)

    return render(request, 'UserStories/importar_tipoUS.html',contexto)


def ver_product_backlog(request,id):
    """
    Vista que permite visualizar los user stories asignados del proyecto
    en el product Backlog
      Argumentos:
          request: HttpRequest
          id : id del proyecto
        Retorna:
          HttpResponse
    """
   
    proyecto = get_object_or_404(Proyecto,id=id)
    us = list(UserStories.objects.filter(id_proyecto = proyecto.id))
    contexto = {'proyecto':proyecto,'us':us}
     
    return render(request,'UserStories/ver_product_backlog.html',contexto)


def listarTipoUS(request,id):
    """
    Vista que permite visualizar los tipos user stories asignados del proyecto
      Argumentos:
          request: HttpRequest
          id : id del proyecto
        Retorna:
          HttpResponse
    """
   
    proyecto = get_object_or_404(Proyecto,id=id)
    tipoUS = proyecto.tipo_us.all() 
    contexto = {'proyecto':proyecto,'tiposUS':tipoUS}
     
    return render(request,'UserStories/listarTipoUS.html',contexto)

def tablaKanban(request, id_tipoUs, id_proyecto):
    """
    Vista que permite visualizar los estados de un user story
      Argumentos:
          request: HttpRequest
          id_tipoUs : id del tipo de user story
        Retorna:
          HttpResponse
    """
    tipoUS = get_object_or_404(TipoUSerStory,id=id_tipoUs)
    estados = tipoUS.estados_kanban.all()
    userstories = UserStories.objects.filter(id_proyecto = id_proyecto).filter(tipo=tipoUS)
    contexto = {'tipoUS':tipoUS,'estados':estados ,'userstories':userstories}
    return render(request,'UserStories/tabla_kanban.html',contexto)

def cambiarEstado(request,id_us,id_estado):
    """
    Vista que permite cambiar el estado de un user story
      Argumentos:
          request: HttpRequest
          id_us : id del user story
          id_estado : id del estado
        Retorna:
          HttpResponse
    """
    us = get_object_or_404(UserStories,id_us=id_us)
    estado = get_object_or_404(Estados_Kanban,id=id_estado)
    us.estado = estado
    us.save()
    return redirect('tabla_kanban',id_tipoUs=us.tipo.id,id_proyecto=us.id_proyecto)