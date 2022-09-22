from django.db import models
from UserStories.models import UserStories
 
# Create your models here.
class estadoSprint(models.TextChoices):
    """
    Modelo que representa los estados posibles de un sprint.
    """
    EN_PLANIFICACION = "En Planificacion"
    EN_EJECUCION = "En curso"
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
    fecha_inicio = models.DateField("Fecha de inicio")
    fecha_fin = models.DateField("Fecha de fin")
    descripcion = models.TextField(max_length=200,blank=True,default='')
    #Almacena la fecha en la que originalmente se planeó terminar el sprint
    #fecha_finalizacion_original= models.DateField(null=True) #Solo es necesario para el Grafico del Burndown Chart
    historias = models.ManyToManyField(UserStories,blank=True)
    estado_sprint = models.CharField(max_length=20, choices=estadoSprint.choices, 
                    default=estadoSprint.EN_PLANIFICACION) #El estado por defecto al empezar es En Planificacion

    def __str__(self):
        return self.nombre_sprint

    def validar(self):
        """
        Metodo del modelo de Sprint que retorna un booleano en caso
        que no se hayan completado los campos obligatorios en el sprint.
        """

        if not self.id_sprint:
            return False
        if not self.nombre_sprint:
            return False   
        if not self.duracion_sprint:
            return False                     
        if not self.fecha_inicio:
            return False
        if not self.fecha_fin:
            return False
        return True