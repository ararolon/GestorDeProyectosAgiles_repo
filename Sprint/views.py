from django.shortcuts import render, redirect,reverse, get_object_or_404
from Sprint.forms import MiembroSprintForm, crearSprintForm, modificarSprintForm
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages
from Proyectos.models import Proyecto
from Sprint.models import Sprint,estadoSprint, SprintMiembros
from UserStories.models import UserStories, HoraPorDia
from Usuarios.models import Usuario,Notificaciones
# Create your views here.
from datetime import datetime
from Proyectos.models import historia


def notificacion(mensaje,usuario,proyecto):
  
  """
  Funcion donde se crean los objetos para las notificaciones
   Arguementos:
      mensaje : lo que se guardara como notificacion
      usuario : el usuario que recibira la notificacion 
      proyecto : el nombre del proyecto asociado a la notificacion
  """

  N = Notificaciones.objects.create(usuario=usuario,mensaje=mensaje)
  N.proyecto = proyecto
  N.save()




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
            mensaje = str(request.user)+ " ha creado el "+str(sprint.nombre_sprint)
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " creó el sprint  "+str(sprint)
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()
            for m in proyecto.miembros.all():
                notificacion(mensaje,m,proyecto.nombre)

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
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " modifico el "+str(s)
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()
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
            miembro = form.cleaned_data['miembro']
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
            h = historia.objects.create(id_proyecto = proyecto.id)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " asignó al miembro  "+str(miembro)+" al "+str(sprint) 
            mensaje =  str(request.user)+" te ha asignado al "+str(sprint.nombre_sprint)
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()
            notificacion(mensaje,miembro,proyecto.nombre)
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
    sprint = proyecto.sprint.all().order_by('-fecha_creacion')
    hayPlanificacion = proyecto.sprint.filter(estado_sprint=estadoSprint.EN_PLANIFICACION).exists()
    hayCurso = proyecto.sprint.filter(estado_sprint=estadoSprint.EN_EJECUCION).exists()
    sprintMiembros = SprintMiembros.objects.filter(proyecto=proyecto) 
    
    contexto = {
        'sprintMiembros':sprintMiembros,
        'sprint':sprint,
        'proyecto':proyecto,
        'hayPlanificacion':hayPlanificacion,
        'hayCurso':hayCurso,
    }
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
    proyecto = get_object_or_404(Proyecto,id = sprint.id_proyecto)
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " inicio el "+str(sprint)
    mensaje = "El " +str(sprint.nombre_sprint)+ " ha iniciado"
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()
    messages.success(request,"El sprint ha iniciado satisfactoriamente")

    return redirect('listarSprint',sprint.id_proyecto)


def cancelarSprint(request):
    """
    Vista donde el Scrum master puede cancelar un sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    id_sprint = int(request.POST.get('sprintId')[0])
    sprint = get_object_or_404(Sprint, id=id_sprint)
    sprint.estado_sprint = 'Cancelado'
    sprint.fecha_fin = timezone.now()
    sprint.save()
    proyecto = get_object_or_404(Proyecto,id = sprint.id_proyecto)
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " cancelo el "+str(sprint)
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()
    messages.success(request,"El sprint ha sido cancelado")
    return redirect('listarSprint',sprint.id_proyecto)


def finalizarSprint(request):
    """
    Vista donde el Scrum master puede finalizar un sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    id_sprint = int(request.POST.get('sprintId')[0])
    sprint = get_object_or_404(Sprint, id=id_sprint)
    sprint.estado_sprint = 'Finalizado'
    sprint.fecha_fin = timezone.now()
    sprint.save()
    proyecto = get_object_or_404(Proyecto,id=sprint.id_proyecto)
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " finalizo el "+str(sprint)
    mensaje = str(request.user)+ "ha finalizado el "+str(sprint.nombre_sprint)
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()
    messages.success(request, "El sprint ha finalizado exitosamente")
    return redirect('listarSprint',sprint.id_proyecto)            


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
        proyecto = get_object_or_404(Proyecto,id = sprint.id_proyecto)
        h = historia.objects.create(id_proyecto = proyecto.id)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        evento = dt_string+","+str(request.user) + " asigno el user story "+str(us)+" al "+str(sprint)
        h.evento = evento
        h.save()
        proyecto.historial.add(h)
        proyecto.save()
    
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
    proyecto = get_object_or_404(Proyecto,id = sprint.id_proyecto)
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " desasigno el user story "+str(us)+" del "+str(sprint)
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()
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
    contexto = {'sprint':sprint, 'miembros':proyecto.miembros.all(), 'id':id, 'proyecto':proyecto,}

    return render(request,'Sprint/sprintbacklog.html',contexto)


def asignarHistoria(request, id_sprint):
    """
    vista que permite asignar un US a un miembro del proyecto asignado a un sprint
        Argumentos:
                request: Objeto HttpRequest
                id_sprint : id del sprint
        Retorna:
            HttpResponse
    """

    user_id = int(request.POST.get('user_id')[0])
    id_us = int(request.POST['usId'])
    us = UserStories.objects.get(id_us=id_us)
    user = Usuario.objects.get(id=user_id)
    us.miembro_asignado = user
    us.save()
    sprint = Sprint.objects.get(id=id_sprint)
    proyecto = get_object_or_404(Proyecto,id = sprint.id_proyecto)
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " asigno el user story "+str(us)+" al miembro "+str(user)+" en el "+str(sprint)
    mensaje = str(request.user)+ " te ha asignado el US :"+str(us.nombre)
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()
    messages.success(request,"US asignado correctamente")
    notificacion(mensaje,user,proyecto.nombre)
    return redirect('sprintbacklog', id = id_sprint)


def burnDownChart(request,id):
    """
    Vista que permite ver el grafico burndownchart de un sprint

    Argumentos:
        request : HttRequest
        id : id del sprint

    Retorna:
         HttpResponse    
    """
    sprint = Sprint.objects.get(id=id)
    historias = sprint.historias.all()
    duracionIdeal = 0
    for historia in historias:
        duracionIdeal = duracionIdeal + historia.horas_estimadas

    duracion = sprint.duracion_sprint
    dias = []
    for i in range(1,duracion+1):
        horaXus = HoraPorDia.objects.filter(dia=i, user_story__in=historias )

        total = 0
        for hora in horaXus:
            total = total + hora.horas

        dias.append(total)

    dias_acumulados = [duracionIdeal]
    for dia in dias:
        aux = dias_acumulados[-1]-dia
        if aux < 0:
            aux = 0
        dias_acumulados.append(aux)

    
    proyecto = Proyecto.objects.get(id=sprint.id_proyecto)
    contexto = {'sprint':sprint, 'miembros':proyecto.miembros.all(), 'id':id, 'proyecto':proyecto,
        'dias':dias, 'dias_acumulados':dias_acumulados, 'duracion':duracion}
    

    return render(request,'Sprint/burnDownChart.html',contexto)
