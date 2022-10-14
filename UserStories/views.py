from multiprocessing import context
from re import U
from django.shortcuts import render, redirect, get_object_or_404

from UserStories.models import TipoUSerStory, UserStories
from .form import EstadosKanbanForm,TiposUSForm, UserStoryForm,ImportarTipoUSForm,ModificarTipoUSForm,ModificarUSForm
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
            us.Prioridad = (((0.6)*us.PN)+((0.4)*us.PT)+us.PS)
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


def modificar_tipoUS(request,id,id_tipo):
    """
    Funcion que permite la modificacion del nombre y la descripciond de un User Story
     Argumentos:
          request: HttpRequest
          id : id del proyecto
          id_tipo :  id del tipo de user story que sera modificado
        Retorna:
          HttpResponse
    """

    proyecto = get_object_or_404(Proyecto,id=id)
    tipo = TipoUSerStory.objects.get(id=id_tipo)       
    
    #un auxiliar para determinar si el tipo de US ya esta asignado
    aux = UserStories.objects.create(nombre="auxiliar")
    aux.save()
    
    #pregunta si el tipo de US esta siendo usado antes de ser modificado
    if aux.es_usado(tipo.id):
        messages.error(request,"El tipo de US no puede modificarse, esta siendo usado")
        aux.delete()
        return redirect('listarTipoUS',id=id)        
    
    aux.delete()

    if request.method == 'POST':
        form = ModificarTipoUSForm(request.POST,instance = tipo)

        if form.is_valid():
            t = form.save()
            t.save()
            messages.success(request,"El tipo de US "+tipo.nombre+" se ha modificado satisfactoriamente")
            return redirect('listarTipoUS',id=id)
        else:
            messages.error(request,"El tipo de US no ha sido modificado")
          
        contexto = { 'proyecto': proyecto,
                     'form': form
                    }
    else:
        contexto = { 'proyecto': proyecto,
                     'form': ModificarTipoUSForm(instance=tipo, initial={'estados_kanban':[a.id for a in tipo.get_estados_kanban()]})
                    }
        
    return render(request,'UserStories/modificar_tipoUS.html',contexto)
        

def eliminar_tipoUS(request,id,id_tipo):
    """
    Vista para eliminar un Tipo de US del proyecto
    Argumentos:
    request: HttpRequest
    id: id del proyectp
    id_tipo: ide del tipo de user story que sera eliminado del proyecto 
    
    Retorno
        HttpResponse
    """

    proyecto = get_object_or_404(Proyecto,id=id)
    tipo = TipoUSerStory.objects.get(id=id_tipo)       
    #un auxiliar para determinar si el tipo de US ya esta asignado
    aux = UserStories.objects.create(nombre="auxiliar")
    aux.save()

    if aux.es_usado(tipo.id):
        messages.error(request,"El tipo de US no puede eliminarse, esta siendo usado")
        aux.delete()
        return redirect('listarTipoUS',id=id)  
    
    contexto = {'proyecto':proyecto,'tipoUS':tipo}
    aux.delete()

    if request.method == 'POST':
            proyecto.tipo_us.remove(tipo)
            messages.success(request,"El tipo "+tipo.nombre+" ha sido eliminado satisfactoriamente del proyecto")
            return redirect('listarTipoUS',id=id)
    
    return render(request,'UserStories/eliminar_tipoUS.html',contexto)


def modificarUS(request,id_proyecto,id):
    """
    Vista que permite modificar un US que todavia no se encuentra asignado a un Sprint
    con esta vista ,se permite ingresar las horas estimadas de un User story

    Argumentos:
        id_proyecto : id del proyecto
        id :  id del US
    
    Retorno
        HttpResponse
    """

    proyecto = get_object_or_404(Proyecto,id=id_proyecto)
    us = UserStories.objects.get(id_us=id)
    
    # verfica si es que el US se encuentra ya asignado a un sprint 
    if us.en_sprint == True:
        messages.error(request,"El  US no puede modificarse, esta siendo usado en un sprint")
        return redirect('product_backlog',id=id_proyecto)

    else:    
        
        if request.method == 'POST':
            form = ModificarUSForm(request.POST,instance = us)

            if form.is_valid():
                u = form.save()
                u.save()
                messages.success(request,"El US "+u.nombre+" se ha modificado satisfactoriamente")
                return redirect('product_backlog',id=id_proyecto)
            else:
                messages.error(request,"El US no ha sido modificado")
            
            contexto = { 'proyecto': proyecto,
                        'form': form
                        }
        else:
            contexto = { 'proyecto': proyecto,
                        'form': ModificarUSForm(instance=us)
                        }
        
    return render(request,'UserStories/modificarUS.html',contexto)
        






