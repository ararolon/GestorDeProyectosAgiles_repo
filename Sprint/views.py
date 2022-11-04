from django.shortcuts import render, redirect,reverse, get_object_or_404
from Sprint.forms import AsignarUSMiembroForm, MiembroSprintForm, crearSprintForm, modificarSprintForm
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages
from Proyectos.models import Proyecto
from Sprint.models import Sprint,estadoSprint, SprintMiembros
from UserStories.models import UserStories
from Usuarios.models import Usuario
# Create your views here.
from datetime import datetime
from Proyectos.models import historia

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
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " creó el "+str(sprint)
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()
               
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



def index_asignar(request,id_sprint):
  """
  Vista que muestra todos los us del proyecto para ser asignados al sprint
  Argumentos:
    request: HttpRequest
    return: HttpResponse
  """

  sprint = Sprint.objects.get(id = id_sprint)
  proyecto = Proyecto.objects.get(id = sprint.id_proyecto)
  historias = UserStories.objects.filter(id_proyecto = proyecto.id).order_by('-Prioridad')
  suma = 0
  contexto = {'user': request.user,'sprint':sprint,'proyecto':proyecto,'historias': historias,'suma':suma}
 
  return render(request,'Sprint/asignarUS.html',contexto)      
            

def asignar_us(request,nombre,id_sprint):
  """
   Vista para que un US sea asignado a un sprint
    Argumentos:
    request: HttpRequest
    nombre : nombre del US
    id_sprint: id del sprint 

    return: HttpResponse
  """
  us = get_object_or_404(UserStories,nombre=nombre)
  sprint = get_object_or_404(Sprint,id=id_sprint)
  suma = 0
  sprint.capacidad_us = 0
  sprint.save()
  

  for s in sprint.historias.all() :
        suma = suma +  s.horas_estimadas
        sprint.capacidad_us = suma
        sprint.save()


  sprint.capacidad_us = sprint.capacidad_us + us.horas_estimadas
  sprint.save()
  print("horas:",sprint.capacidad_us)
  print("capacidad",sprint.capacidad)

  if not sprint.capacidad_us > sprint.capacidad:
        us.en_sprint = True
        us.PS = us.PS + 3 # se agrega la capacidad de US dentro del sprint
        us.save()
        sprint.historias.add(us)
        sprint.save()
        messages.success(request,"Los user story asignado exitosamente")
    
  else:
          messages.error(request,'Supera la capacidad de este sprint')

  return redirect('indexasignar',id_sprint=id_sprint)


def desasignar_us(request,nombre,id_sprint):
    """
    Vista que permite quitar un US del sprint backlog
    Argumentos:
    request: HttpRequest
    nombre : nombre del US
    id_sprint: id del sprint 

    return: HttpResponse
    """

    us = get_object_or_404(UserStories,nombre=nombre)
    us.en_sprint = False
    us.save()
    sprint = get_object_or_404(Sprint,id=id_sprint)

    sprint.historias.remove(us)
    sprint.save()
    messages.success(request,"User storie desasignado exitosamente")

    return redirect('indexasignar',id_sprint=id_sprint)







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
    proyecto = Proyecto.objects.get(id=sprint.id_proyecto)
    contexto = {'sprint':sprint, 'miembros':proyecto.miembros.all(), 'id':id}

    return render(request,'Sprint/sprintbacklog.html',contexto)

def asignarHistoria(request, id_sprint):

    print("entro")
    print(request.POST)

    user_id = int(request.POST.get('user_id')[0])
    id_us = int(request.POST['usId'][0])
    us = UserStories.objects.get(id_us=id_us)
    user = Usuario.objects.get(id=user_id)
    us.miembro_asignado = user
    us.save()
    print(us)

    return redirect('sprintbacklog', id = id_sprint)
