from multiprocessing import context
from re import U
from time import timezone
from django.shortcuts import render, redirect, get_object_or_404

from UserStories.models import Estados_Kanban, TipoUSerStory, UserStories, HoraPorDia
from .form import EstadosKanbanForm, ModificarUSForm,TiposUSForm, UserStoryForm,ImportarTipoUSForm, ModificarTipoUSForm
from django.contrib import messages
from Proyectos.models import Proyecto, historia
from Sprint.models import Sprint, estadoSprint
from datetime import datetime


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
            e = form.cleaned_data['nombre']
            fecha = datetime.now()
            h = historia.objects.create(id_proyecto = proyecto.id)
            evento = str(fecha.day)+"/"+str(fecha.month)+"/"+str(fecha.year)+" "+str(fecha.hour)+":"+str(fecha.minute)+":"+str(fecha.second)+","+str(request.user) + " creó el estado kanban " + e + " para el proyecto "
            h.evento = evento
            h.save()
            estado = form.save()
            estado.save()
            messages.success(request,"El estado "+estado.nombre+ " ha sido creado satisfactoriamente")
            proyecto.historial.add(h)
            proyecto.save()
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
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " creó el tipo de User Story "+str(tipoUS)+" en el proyecto"
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()
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
            us.id_proyecto = proyecto.id
            us.Prioridad = (((0.6)*us.PN)+((0.4)*us.PT)+us.PS)
            us.save()
            messages.success(request,"El User Story "+us.nombre+" ha sido creado satisfactoriamente")
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " creó el User Story "+str(us)+" en el proyecto"
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()
            return redirect('product_backlog',id=proyecto.id)
                
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
            for t in proyecto.tipo_us.all():
                h = historia.objects.create(id_proyecto = proyecto.id)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " importó el tipo de User Story "+str(t)+" en el proyecto"
                h.evento = evento
                h.save()
                proyecto.historial.add(h)
                proyecto.save()


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
    contexto = {'proyecto':proyecto,'us':us,}
     
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

def tablaKanban(request, id_proyecto):
    """
    Vista que permite visualizar los estados de un user story
      Argumentos:
          request: HttpRequest
          id_proyecto : id del proyecto
        Retorna:
          HttpResponse
    """
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    tipos = proyecto.tipo_us.all()
    if not tipos:
        messages.error(request,"No hay tipos de User Story creados")
        return render(request, 'proyectos/mostrarProyecto.html', {'proyecto':proyecto})
    estados = tipos.first().estados_kanban.all()
    sprint = Sprint.objects.filter(id_proyecto=proyecto.id).filter(estado_sprint = "En Curso").first()
    
    if not sprint:
        messages.error(request,"No hay un sprint en Curso")
        return render(request, 'proyectos/mostrarProyecto.html', {'proyecto':proyecto})
    userstories = sprint.historias.all()
    contexto = {'tipos':tipos,'estados':estados ,'userstories':userstories, 'proyectoActual':proyecto.id}
    if request.method == "POST":
        id_us = int(request.POST['usId'])
        id_estado = int(request.POST['estadoId'])
        # horas = request.POST['horas']
        actividad = request.POST['actividad']

        us = get_object_or_404(UserStories,id_us=id_us)
        estado = get_object_or_404(Estados_Kanban,id=id_estado)
        proyecto = get_object_or_404(Proyecto,id=us.id_proyecto)

        if (not proyecto.scrumMaster == request.user and not id_estado > us.estado.id):
            messages.error(request,'Solo el scrummaster puede realizar esa operacion')
            return redirect('tabla_kanban',id_proyecto=proyecto.id)
        # if (horas == ""):
        #     messages.error(request,'No puede quedar vacio el campo de horas')
        #     return redirect('tabla_kanban',id_proyecto=proyecto.id)
        # # horas trabajas mayor a horas de esfuerzo
        # if (int(horas) > us.horas_estimadas):
        #     messages.error(request,'No puede ingresar mas horas, horas trabajabas no puede ser mayor a horas de esfuerzo')
        #     return redirect('tabla_kanban',id_proyecto=proyecto.id)

        us.estado = estado
        # us.horas = horas
        # us.horas_trabajadas += int(horas)
        us.actividad = actividad
        us.responsable = request.user
        us.save()
        return redirect('tabla_kanban',id_proyecto=proyecto.id)
        

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
    proyecto = get_object_or_404(Proyecto,id=us.id_proyecto)

    if (not proyecto.scrumMaster == request.user and not id_estado > us.estado.id):
        messages.error(request,'Solo el scrummaster puede realizar esa operacion')
        return redirect('tabla_kanban',id_proyecto=proyecto.id)

    us.estado = estado
    us.save()
    return redirect('tabla_kanban',id_proyecto=proyecto.id)

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
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " modificó el tipo de user story "+str(tipo.nombre)
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()

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
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " eliminó el tipo de user story "+str(tipo.nombre)+" del proyecto"
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()


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
                h = historia.objects.create(id_proyecto = proyecto.id)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " modificó el user story "+str(us)
                h.evento = evento
                h.save()
                proyecto.historial.add(h)
                proyecto.save()
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


def cancelar_US(request,id):
  """
    Funcion que permite cancelar un US

     Argumentos:
        id :  id del US
    
    Retorno
        HttpResponse

  """
 
  if request.method == 'POST':
        motivo = request.POST['motivo_cancelacion']
        
        us = get_object_or_404(UserStories,id_us=id)
        estado = Estados_Kanban.objects.get(nombre="Cancelado")      
        us.estado= estado
        us.motivo_cancelacion = motivo
        us.save()
        proyecto = get_object_or_404(Proyecto,id = us.id_proyecto)
        h = historia.objects.create(id_proyecto = proyecto.id)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        evento = dt_string+","+str(request.user) + " canceló el user story "+str(us)
        h.evento = evento
        h.save()
        proyecto.historial.add(h)
        proyecto.save()
               
        return redirect('product_backlog',id = us.id_proyecto)

def cargarHoras(request):
    """
    Vista que permite cargar las horas de un US
    
    Retorno
        HttpResponse

  """
    if request.method == 'POST':
        horas = request.POST['horas']
        horas = int(horas)
        id_us = request.POST['usId']
        id_us = int(id_us)
        us = UserStories.objects.get(id_us=id_us) 
        horaXus = HoraPorDia.objects.filter(user_story=us).last()
       
        sprint = Sprint.objects.get(historias__id_us=id_us)
        duracion_sprint = sprint.duracion_sprint

        if horaXus: 
            siguienteDia = horaXus.dia+1 
        else :
            siguienteDia = 1

        if siguienteDia > duracion_sprint:
            messages.error(request,"No se puede cargar mas horas, el sprint ya no tiene dias disponibles")
            return redirect('tabla_kanban',id_proyecto=us.id_proyecto)

        
        HoraPorDia.objects.create(horas=horas, user_story=us, dia=siguienteDia)
        messages.success(request,"Se han cargado las horas correctamente")
        horasDelSprint = HoraPorDia.objects.filter(user_story=us)
        horasTotales = 0
        for hora in horasDelSprint:
            horasTotales += hora.horas
        us.horas_trabajadas = horasTotales
        us.save()   

        return redirect('tabla_kanban',id_proyecto=us.id_proyecto)
