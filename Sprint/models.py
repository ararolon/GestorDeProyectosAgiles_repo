from email.policy import default
from django.db import models
from django.utils import timezone
from UserStories.models import UserStories
from Usuarios.models import Usuario
 
# Create your models here.
class estadoSprint(models.TextChoices):
    """
    Modelo que representa los estados posibles de un sprint.
    """
    EN_PLANIFICACION = "En Planificacion"
    EN_EJECUCION = "En Curso"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"
 
class Sprint(models.Model):
 
    """
    Modelo que representa Sprint en el sistema, debe ser creado por un usuario con el permiso correspondiente
    Clase de Sprint: almacena datos generales acerca del sprint de un proyecto.
    Clase Padre: models.Model
    """

    id_sprint = models.CharField(max_length=100)
    nombre_sprint = models.CharField(max_length=100,unique=True,blank=False)
    duracion_sprint = models.IntegerField("Duración del sprint", blank=True, null=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now)
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de inicio", null=True, blank=True)
    fecha_fin = models.DateTimeField(verbose_name="Fecha de fin",null=True, blank=True)
    descripcion = models.TextField(max_length=200,blank=True,default='')
    #Almacena la fecha en la que originalmente se planeó terminar el sprint
    #fecha_finalizacion_original= models.DateField(null=True) #Solo es necesario para el Grafico del Burndown Chart
    historias = models.ManyToManyField(UserStories,blank=True)
    estado_sprint = models.CharField(max_length=20, choices=estadoSprint.choices, 
                    default=estadoSprint.EN_PLANIFICACION) #El estado por defecto al empezar es En Planificacion
    id_proyecto = models.IntegerField(null=True)
    miembros_sprint = models.ManyToManyField(Usuario, related_name='set_miembros_sprint')
    capacidad = models.IntegerField(verbose_name='Capacidad en horas', null=True, blank=False)
    capacidad_us = models.IntegerField(default=0,blank=False)
    
    def __str__(self):
        return self.nombre_sprint

    def cancelar_sprint(self):
        if self.estado_sprint == estadoSprint.FINALIZADO:
            return False
        else:
            self.estado_sprint = estadoSprint.CANCELADO
        return True

    def validar(self):
        """
        Metodo del modelo de Sprint que retorna un booleano en caso
        que no se hayan completado los campos obligatorios en el sprint.
        """
        
        if not self.nombre_sprint:
            return False   
        if not self.duracion_sprint:
            return False     
        if not self.fecha_creacion:
            return False                    
        if not self.fecha_inicio:
            return False
        if not self.fecha_fin:
            return False
        return True

    def sprintMiembros(self):
        """
        Metodo del modelo Sprint que retorna los miembros de un Sprint
        """
        return self.miembros_sprint
    
    