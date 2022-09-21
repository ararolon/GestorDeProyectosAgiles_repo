from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Usuarios.models import Usuario



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
    estado = models.CharField(max_length=20, verbose_name="Estado actual del Proyecto")
    miembros = models.ManyToManyField(Usuario, related_name='set_miembros')
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


class estadoProyecto:
   
    PLANIFICACION = "En Planificacion"
    ENEJECUCION = "En curso"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"


