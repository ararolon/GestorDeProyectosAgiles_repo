from urllib import request
from django.shortcuts import render, redirect,reverse, get_object_or_404
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


def listarProyectos(request):
    """
    Vista que muestra al usuario la lista de Proyectos que existen dentro del Sistema.
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    contexto = {
                'proyectos': [
                    {'id': Proyecto.id_proyecto, 'nombre': Proyecto.nombre, 'descripcion': Proyecto.descripcion, 
                  #  'url': reverse('mostrarUnProyecto', args=(Proyecto.id_proyecto))
                     }
                    for Proyecto in Proyecto.objects.all()
                ],
                
                }
    mostrarUnProyecto(id)
    return render(request, 'proyectos/listarProyectos.html', contexto)

id_proyecto=Proyecto.id_proyecto

def mostrarUnProyecto(request, id_proyecto):
   
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    
    contexto = {'user': request.user,
                #'id': Proyecto.id_proyecto,
                'proyecto': proyecto,
                }
    return render(request, 'proyectos/mostrarUnProyecto.html', contexto)