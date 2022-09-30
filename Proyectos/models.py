from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Sprint.models import Sprint
from Usuarios.models import Usuario
from permisos.models import RolesdeSistema
from UserStories.models import UserStories,TipoUSerStory

class estadoProyecto:
   
    PLANIFICACION = "En Planificacion"
    ENEJECUCION = "En Curso"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"

estado_choices = (
        (estadoProyecto.PLANIFICACION, 'En Planificacion'),
        (estadoProyecto.ENEJECUCION, 'En Curso'),
        (estadoProyecto.FINALIZADO, 'Finalizado'),
        (estadoProyecto.CANCELADO, 'Cancelado'),
    )

class RolUsuario(models.Model):
    """
    Modelo para la clase de RolUsuario con los campos necesarios para el mismo
    """
    miembro = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    roles = models.ManyToManyField(RolesdeSistema)   
 


class Proyecto(models.Model):
    """
        Modelo para la clase de Proyecto con los campos necesarios para el mismo
    """
    id_proyecto = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)
    scrumMaster = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    fecha_de_inicio = models.DateTimeField(verbose_name="Fecha de Inicio del proyecto", default=timezone.now)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=estado_choices, 
                    default=estadoProyecto.PLANIFICACION)
    miembros = models.ManyToManyField(Usuario, related_name='set_miembros')
    roles = models.ManyToManyField(RolesdeSistema)
    usuario_roles = models.ManyToManyField(RolUsuario)
    tipo_us = models.ManyToManyField(TipoUSerStory)
    sprint = models.ManyToManyField(Sprint) 

    #id_sprints = models.ManyToManyField(Sprint, blank=True) -->preguntar
    #tipoUS = models.CharField(max_length=100, verbose_name="Tipos de US") -->preguntar bien como hacer y como se llama en esta clase


    def __str__(self):
        return self.nombre


    def get_scrumMaster(self):
        """
        Metodo que retorna el Usuario del Scrum Master del proyecto
        """
        return self.scrumMaster

    def miembros_proyecto(self):
        
        miembros = [self.set_miembros.get(usuario=self.scrumMaster)]
        miembros.extend(list(self.set_miembros.all().filter(rol__isnull=False)))

        return miembros


    def cancelar(self):
        if self.estado == estadoProyecto.FINALIZADO:
            return False
        else:
            self.estado = estadoProyecto.CANCELADO
        return True




