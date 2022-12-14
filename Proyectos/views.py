from urllib import request
from django.shortcuts import render, redirect,reverse, get_object_or_404
from Proyectos.forms import AsignarMiembroForm, AsignarRolForm, ImportarRolForm, crearproyectoForm
from Proyectos.models import Proyecto, RolUsuario, historia
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib import messages
from Usuarios.models import Usuario, Notificaciones
from permisos.models import RolesdeSistema
from datetime import datetime
# Create your views here.

def notificacion(mensaje,usuario,proyecto):
  
  """
  Funcion donde se crean los objetos para las notificaciones
   Arguementos:
      mensaje : lo que se guardara como notificacion
      usuario : el usuario que recibira la notificacion 
      proyecto : el nombre del proyecto asociado a la notificacion
  """
  N = Notificaciones.objects.create(usuario=usuario,mensaje=mensaje,proyecto=proyecto)






def crearProyecto (request):
    """
    Metodo para crear proyecto
    param request: request para datos nuevos de un proyecto
    return: contexto para proyecto nuevo
    """


    if request.method == 'POST':
        form = crearproyectoForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['scrumMaster']
            proyecto = form.save(commit=False)
            proyecto.fecha_de_inicio = timezone.now()
            proyecto.save()
            rol = RolesdeSistema.objects.get(nombre='Scrum Master')
            user.asignar_rol_a_usuario(rol.id)
            messages.success(request,"Se ha creado el proyecto satisfactoriamente")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " creó el proyecto " + proyecto.nombre
            h = historia.objects.create(id_proyecto = proyecto.id)
            h.evento = evento
            h.save()
            proyecto.historial.add(h)
            proyecto.save()
            # para notificar al scrum master 
            mensaje = str(request.user)+" te ha asignado como scrum master del proyecto: "+str(proyecto.nombre)
            notificacion(mensaje,proyecto.scrumMaster,proyecto.nombre)
            return redirect('home')
    else:
         form = crearproyectoForm()
    contexto = {'form': form
                }
    return render(request,'proyectos/crearProyectos.html',context=contexto)    


def listarProyectos(request):
    """
    Vista que muestra al Administrador del sistema la lista de Proyectos que existen dentro del Sistema.
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    # los proyectos aceptados son los que el usuario:
    # 1 es scrum master o
    # 2 miembro
    proyectos = Proyecto.objects.all()
    contexto = {
        'proyectos': [
            {
                'id': Proyecto.id,
                'nombre': Proyecto.nombre,
                'descripcion': Proyecto.descripcion,
                'scrumMaster': Proyecto.scrumMaster,
            } for Proyecto in proyectos
        ],
    }
    return render(request, 'proyectos/listarProyectos.html', contexto)

def listarProyectosUser(request):
    """
    Vista que muestra al usuario la lista de Proyectos que existen dentro del Sistema.
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    # los proyectos aceptados son los que el usuario:
    # 1 es scrum master o
    # 2 miembro
    proyectos = (
        Proyecto.objects.filter(miembros__id=request.user.id) 
        | Proyecto.objects.filter(scrumMaster=request.user.id)
    ).distinct() # para que no se repitan los proyectos

    contexto = {
        'proyectos': [
            {
                'id': Proyecto.id,
                'nombre': Proyecto.nombre,
                'descripcion': Proyecto.descripcion,
                'scrumMaster': Proyecto.scrumMaster,
            } for Proyecto in proyectos
        ],
    }
    return render(request, 'proyectos/listarProyectosUser.html', contexto)

def mostrarProyectoAdmin(request, id_proyecto):
    """
    Vista donde el admin puede ver los detalles del proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    # form = AsignarMiembroForm(instance=proyecto)
    # if request.method == 'POST':
    #     form = AsignarMiembroForm( instance=proyecto, data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Los miembros han sido asignado al proyecto')
    #         return redirect('home')
    contexto = {
        # 'form': form,
        'proyecto': proyecto,
    }
    return render(request, 'proyectos/mostrarProyectoAdmin.html', contexto)

    

def asignar_miembro(request, id_proyecto):
    """
    Vista que donde el Scrum master puede seleccionar los participantes del proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    print(id_proyecto)
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    form = AsignarMiembroForm(instance=proyecto)
    if request.method == 'POST':
        form = AsignarMiembroForm( instance=proyecto, data=request.POST)
        if form.is_valid():
            miembros = form.cleaned_data['miembros']
            form.save()
            messages.success(request, 'Los miembros han sido asignado al proyecto')
            h = historia.objects.create(id_proyecto = proyecto.id)
            mensaje = str(request.user)+" te ha asignado como miembro del proyecto: "+str(proyecto.nombre)
            for m in miembros :
                h = historia.objects.create(id_proyecto = proyecto.id)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " asignó a " + str(m) + " al proyecto "
                h.evento = evento
                h.save()
                proyecto.historial.add(h)
                proyecto.save()
                notificacion(mensaje,m,proyecto.nombre)
                
            return redirect('mostrarProyecto', id_proyecto=id_proyecto)
    contexto = {
        'form': form,
        'proyecto': proyecto,
    }
    return render(request, 'proyectos/asignar_miembro.html', contexto)

def asignarRol(request, id_proyecto, id_usuario):
    """
    Vista que donde el Scrum master puede seleccionar el rol a asignar a un usuario dentro del proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    
    """
   
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    usuario_rol = proyecto.usuario_roles.filter(miembro=id_usuario).first()
    if request.method == 'POST':
        form = AsignarRolForm(id_proyecto, id_usuario, request.POST, instance=usuario_rol) 
        if form.is_valid():
            roles = form.cleaned_data['roles']
            usuario_rol = form.save()
            usuario = Usuario.objects.get(id=id_usuario)
            usuario_rol.miembro = usuario
            usuario_rol.save()
            proyecto.usuario_roles.add(usuario_rol)
            messages.success(request,"Se asigno correctamente")
            
            for r in roles :
                h = historia.objects.create(id_proyecto = proyecto.id)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " asignó el rol" + str(r) + " al miembro " + str(usuario)
                mensaje = str(request.user)+" te ha asignado el rol de "+str(r)
                h.evento = evento
                h.save()
                proyecto.historial.add(h)
                proyecto.save()
                notificacion(mensaje,usuario,proyecto.nombre)
                
            return redirect('mostrarProyecto', id_proyecto=id_proyecto)
    else:
        if usuario_rol:
            form = AsignarRolForm(id_proyecto, id_usuario, instance=usuario_rol)
            data = []
            usuario = Usuario.objects.get(id=id_usuario)
            data = usuario_rol
            for r in  data.roles.all(): 
                h = historia.objects.create(id_proyecto = proyecto.id)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " quitó el rol" + str(r) + " al miembro " + str(usuario)
                mensaje = "Se te ha quitado el rol de "+str(r)
                h.evento = evento
                h.save()
                proyecto.historial.add(h)
                proyecto.save()
                notificacion(mensaje,usuario,proyecto.nombre)
        else:
            form = AsignarRolForm(id_proyecto, id_usuario, )
    contexto = {'form': form}
    return render(request, 'proyectos/asignarRol.html', contexto)

def importarRol(request, id_proyecto):
    """
    Vista que donde el Scrum master puede importar el rol dentro de un proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    form = ImportarRolForm(instance=proyecto)
    if request.method == 'POST':
        form = ImportarRolForm( instance=proyecto, data=request.POST)
        if form.is_valid():
            roles = form.cleaned_data['roles']
            form.save()
            messages.success(request, 'Los roles han sido importados satisfactoriamente')
            for r in roles :
                h = historia.objects.create(id_proyecto = proyecto.id)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " importó  el rol " + str(r) + " al proyecto "
                h.evento = evento
                h.save()
                proyecto.historial.add(h)
                proyecto.save()
            return redirect('mostrarProyecto', id_proyecto=id_proyecto)
    contexto = {
        'form': form,
        'proyecto': proyecto,
        'roles': RolesdeSistema.objects.filter(defecto=False)

    }
    return render(request, 'proyectos/importarRol.html', contexto)

def iniciarProyecto(request, id_proyecto):
    """
    Donde el Scrum master puede iniciar un proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    proyecto.estado = 'En Curso'
    proyecto.save()
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " inició " + "el proyecto "
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()
    messages.success(request, 'Proyecto iniciado satisfactoriamente')
    


    return redirect('mostrarProyecto', id_proyecto=id_proyecto)


def cancelarProyecto(request, id_proyecto):
    """
    Donde el Scrum master puede cancelar un proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """

    if request.method == "POST":
        motivo = request.POST['motivo']

    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    proyecto.estado = 'Cancelado'
    proyecto.motivo = motivo
    proyecto.save()
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " canceló el proyecto "
    mensaje = "El proyecto ha sido cancelado"
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()
    #para que llegue a todos los miembros del proyecto
    for m in proyecto.miembros.all() :
        notificacion(mensaje,m,proyecto.nombre)
    
    messages.success(request, 'Proyecto cancelado satisfactoriamente')
    return redirect('mostrarProyecto', id_proyecto=id_proyecto)

def mostrarProyecto(request, id_proyecto):
    """
    Vista donde el Scrum Master visualiza detalles del proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    # form = AsignarMiembroForm(instance=proyecto)
    # if request.method == 'POST':
    #     form = AsignarMiembroForm( instance=proyecto, data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Los miembros han sido asignado al proyecto')
    #         return redirect('home')
    contexto = {
        # 'form': form,
        'proyecto': proyecto,
    }
    return render(request, 'proyectos/mostrarProyecto.html', contexto)


def ver_historial(request,id):
   """
    Vista que permite visualizar el historial del proyecto
       Argumentos:
        request: HttpRequest
        id : id del proyecto
       Return: HttpResponse    
   """
   proyecto = get_object_or_404(Proyecto, id=id)

   eventos = []

   eventos =  proyecto.historial.all().order_by('-id')

   contexto = {'evento':eventos,'proyecto':proyecto}

   return render(request,'proyectos/historial.html',contexto)


def finalizarProyecto(request, id_proyecto):
    """
    Donde el Scrum master puede finalizar un proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    proyecto.estado = 'Finalizado'
    proyecto.save()
    h = historia.objects.create(id_proyecto = proyecto.id)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + " finalizó " + "el proyecto "
    h.evento = evento
    h.save()
    proyecto.historial.add(h)
    proyecto.save()


    return redirect('mostrarProyecto', id_proyecto=id_proyecto)



