from django.shortcuts import render, redirect,reverse, get_object_or_404
from Sprint.forms import AsignarUSMiembroForm, AsignarUSSprintForm, MiembroSprintForm, crearSprintForm, modificarSprintForm
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages
from Proyectos.models import Proyecto
from Sprint.models import Sprint,estadoSprint, SprintMiembros
from UserStories.models import UserStories
# Create your views here.

def crearSprint (request,id):
    """
    Metodo para crear sprint
    param request: request para datos nuevos de un sprint
    return: contexto para sprint nuevo
    """
    proyecto = get_object_or_404(Proyecto,id=id)
    contexto = {'user': request.user,'proyecto':proyecto}
    contexto['form'] = crearSprintForm(proyecto.id)

    if request.method == 'POST':
        form = crearSprintForm(proyecto.id,request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)            
            sprint.id_proyecto = proyecto.id
            sprint.save()
            proyecto.sprint.add(sprint) 
            
            messages.success(request,"Se ha creado el sprint satisfactoriamente")
            return render(request, 'proyectos/mostrarProyecto.html', {'proyecto':proyecto})
    else:
        form = crearSprintForm(proyecto.id)
    contexto = {
        'form': form,
        'proyecto':proyecto
    }
    return render(request,'Sprint/crearSprint.html',context=contexto)    


def modificarSprint(request,id,id_sprint):
    """
    Metodo para modificar el nombre, la descripción y la fecha final de un Sprint
    param request: request para datos actualizados de un sprint
    return: contexto para sprint actualizado
    """
    
    proyecto = get_object_or_404(Proyecto,id=id)
    sprint = Sprint.objects.get(id=id_sprint)
    
    if request.method == 'POST':
        form = modificarSprintForm(request.POST,instance=sprint)        
        if form.is_valid():
            s = form.save()
            s.save()
            messages.success(request,"El Sprint ha sido modificado satisfactoriamente")
            return redirect('listarSprint', id=id)
        else:
            messages.error(request,"El Sprint no ha sido modificado")
        contexto = { 
            'proyecto': proyecto,
            'form': form
        }
    else:
        contexto = {
            'proyecto': proyecto,
            'form': modificarSprintForm(instance=sprint)
        }
    return render(request,'Sprint/modificarSprint.html',contexto)


def asignarMiembroSprint(request,id_sprint):
    """
    Vista para asignar miembros a un Sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """

    sprint = get_object_or_404(Sprint,id=id_sprint)
    proyecto = get_object_or_404(Proyecto,id=sprint.id_proyecto)
    
    contexto = {'user': request.user,'proyecto':proyecto}
    
    suma = 0
    if request.method == 'POST':
        form = MiembroSprintForm(id_sprint,request.POST)
        if form.is_valid():
            f=form.save()  
            f.proyecto=proyecto
            f.save()

            capacidadM = SprintMiembros.objects.filter(sprint=sprint)
                
            for i in capacidadM:
                suma = suma + i.capacidad_miembro
                sprint.capacidad_equipo = suma
            
            sprint.capacidad = sprint.capacidad_equipo*sprint.duracion_sprint
            sprint.save()    
            
            messages.success(request,"Miembro asignado correctamente")
            return redirect('listarSprint', proyecto.id)
    else:
        form = MiembroSprintForm(id_sprint)
    contexto = {
        'form': form,
        'proyecto':proyecto,
        'sprint':sprint
    }
            
    return render(request,'Sprint/asignarMiembroSprint.html',context=contexto)    
    

def listarSprint(request,id):
    """
    Vista que permite visualizar los sprints del proyecto
      Argumentos:
          request: HttpRequest
          id : id del proyecto
        Retorna:
          HttpResponse
    """
   
    proyecto = get_object_or_404(Proyecto,id=id)
    sprint = proyecto.sprint.all().order_by('fecha_creacion')
    hayPlanificacion = proyecto.sprint.filter(estado_sprint=estadoSprint.EN_PLANIFICACION).exists()
    hayCurso = proyecto.sprint.filter(estado_sprint=estadoSprint.EN_EJECUCION).exists()
    sprintMiembros = SprintMiembros.objects.filter(proyecto=proyecto) 
    contexto = {'sprintMiembros':sprintMiembros,'proyecto':proyecto,'sprint':sprint,'hayPlanificacion':hayPlanificacion,'hayCurso':hayCurso}
    return render(request,'Sprint/listarSprint.html',contexto)


def iniciarSprint(request, id_sprint):
    """
    Vista donde el Scrum master puede iniciar un sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    sprint = get_object_or_404(Sprint, id=id_sprint)
    sprint.estado_sprint = 'En Curso'
    sprint.fecha_inicio = timezone.now()
    sprint.save()
    return redirect('listarSprint',sprint.id_proyecto)


def cancelarSprint(request, id_sprint):
    """
    Vista donde el Scrum master puede cancelar un sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    sprint = get_object_or_404(Sprint, id=id_sprint)
    sprint.estado_sprint = 'Cancelado'
    sprint.fecha_fin = timezone.now()
    sprint.save()
    return redirect('listarSprint',sprint.id_proyecto)


def asignar_us(request,id_sprint):
    """
    Vista para que un US sea asignado a un sprint
    Argumentos:
        request: HttpRequest
        return: HttpResponse
    """

    sprint = Sprint.objects.get(id = id_sprint)
    proyecto = Proyecto.objects.get(id = sprint.id_proyecto)
    contexto = {'user': request.user,'sprint':sprint,'proyecto':proyecto}
    contexto['form'] = AsignarUSSprintForm(proyecto,sprint)

    if request.method == 'POST':
            form = AsignarUSSprintForm(proyecto,sprint,instance=proyecto,data=request.POST)
            if form.is_valid():
                historias = form.cleaned_data['historias']
                sprint.historias.set(historias)
            
            # marca los user stories asignados con la bandera para indicar que se encuentran en el sprint 
                for u in historias :
                    u.en_sprint = True
                    u.save()              

                messages.success(request,"Los user stories han sido asignados exitosamente")
                return redirect ('listarSprint',id = proyecto.id)
            else:
                messages.error(request,'Los user stories no pudieron ser asignados')
    else:
            contexto['form'] = AsignarUSSprintForm(proyecto,sprint)

    return render(request,'Sprint/asignarUS.html',contexto)      
            

def asignarUSMiembro(request, id_sprint_miembro):
    """
    Vista en el que se puede seleccionar un US del Sprint Backlog para asignar a un usuario dentro del Sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
   
    sprint_miembro = SprintMiembros.objects.get(id=id_sprint_miembro)
    if request.method == 'POST':
        form = AsignarUSMiembroForm(sprint_miembro.sprint.id,request.POST, instance=sprint_miembro) 
        if form.is_valid():
            us = form.save()
            us.save()
            messages.success(request,"US asignado correctamente")
            return redirect('listarSprint', sprint_miembro.proyecto.id)
    else:
        form = AsignarUSMiembroForm(sprint_miembro.sprint.id,instance=sprint_miembro)
    contexto = {'form': form,'id_proyecto':sprint_miembro.proyecto.id}
    return render(request, 'Sprint/asignar_us_miembro.html', contexto)


def asignar_us(request,id_sprint):
  """
  Vista para que un US sea asignado a un sprint
  Argumentos:
    request: HttpRequest
    return: HttpResponse
  """

  sprint = Sprint.objects.get(id = id_sprint)
  proyecto = Proyecto.objects.get(id = sprint.id_proyecto)
  historias = UserStories.objects.filter(id_proyecto = proyecto.id)
  contexto = {'user': request.user,'sprint':sprint,'proyecto':proyecto,'historias': historias}
  contexto['form'] = AsignarUSSprintForm(proyecto,sprint)
  suma = 0
  if request.method == 'POST':
        form = AsignarUSSprintForm(proyecto,sprint,instance=proyecto,data=request.POST)
        if form.is_valid():
            historias = form.cleaned_data['historias']
            sprint.historias.set(historias)
           
           # marca los user stories asignados con la bandera para indicar que se encuentran en el sprint 
            for u in historias :
                u.en_sprint = True
                u.save()
                suma = suma +  u.horas_estimadas
                sprint.capacidad_us = suma
                sprint.save()
             
            if sprint.capacidad_us > sprint.capacidad:
                messages.error(request,'Supera la capacidad de este sprint')
            else:
                messages.success(request,"Los user stories han sido asignados exitosamente")
                return redirect ('listarSprint',id = proyecto.id)
        else:
            messages.error(request,'Los user stories no pudieron ser asignados')
  else:
         contexto['form'] = AsignarUSSprintForm(proyecto,sprint)

  return render(request,'Sprint/asignarUS.html',contexto)      
            


def ver_sprintbacklog(request,id):
    """
    Vista que permite ver el sprint backlog de un sprint

    Argumentos:
        request : HttRequest
        id : id del sprint

    Retorna:
         HttpResponse    
    """

    sprint = Sprint.objects.get(id=id)
    contexto = {'sprint':sprint}  

    

    return render(request,'Sprint/sprintbacklog.html',contexto)

