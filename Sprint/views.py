from django.shortcuts import render, redirect,reverse, get_object_or_404
from Sprint.forms import MiembroSprintForm, crearSprintForm
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages
from Proyectos.models import Proyecto
from Sprint.models import Sprint,estadoSprint

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
    contexto = {'form': form,
                'proyecto':proyecto
                }
    return render(request,'Sprint/crearSprint.html',context=contexto)    


def mostrarSprint(request):
    """
    Metodo para mostrar sprint.
    Argumentos:
        request: HttpRequest
    Retorna:
        HttpResponse
    """
    contexto = {
        'sprints': [
            {
                'id': sprint.id,
                'id_sprint': sprint.id_sprint, 
                'nombre_sprint': sprint.nombre_sprint,
                'fecha_creacion': sprint.fecha_creacion, 
                'fecha_inicio': sprint.fecha_inicio,
                'fecha_fin': sprint.fecha_fin,
                'descripcion': sprint.descripcion,
                'estado_sprint': sprint.estado_sprint,
            }
            for sprint in Sprint.objects.all()
        ],
    }

    return render(request, 'Sprint/mostrarSprint.html', contexto)

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
    contexto = {'proyecto':proyecto,'sprint':sprint,'hayPlanificacion':hayPlanificacion,'hayCurso':hayCurso}
     
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


def sprint_miembros(request, id_sprint):
    """
    Vista que donde el Scrum master puede seleccionar los participantes del proyecto
    para asignar a un Sprint
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    print('*'*66)
    print(id_sprint)
    sprintM = get_object_or_404(Sprint, id=id_sprint)
    form = MiembroSprintForm(instance=sprintM)
    if request.method == 'POST':
        form = MiembroSprintForm( instance=sprintM, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operación Exitosa')
            return redirect('mostrarSprint')
    contexto = {
        'form': form,
        'sprintM': sprintM,
    }
    return render(request, 'Sprint/sprint_miembros.html', contexto)
