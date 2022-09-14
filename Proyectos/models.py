from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Usuarios.models import Usuario
from permisos.models import RolesdeSistema




    
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
    #id_sprints = models.ManyToManyField(Sprint, blank=True) -->preguntar
    #tipoUS = models.CharField(max_length=100, verbose_name="Tipos de US") -->preguntar bien como hacer y como se llama en esta clase



    def __str__(self):
        return self.nombre


    def get_scrumMaster(self):
        """
        Metodo que retorna el Usuario del Scrum Master del proyecto
        """
        return self.scrumMaster




    def get_miembros_proyecto(self):
        """
        Metodo para obtener los miembros de un proyecto
        Retorna:
            QuerySet: objeto con todos los participantes del Proyecto.
        """
        miembros = [self.set_miembros.get(usuario=self.scrumMaster)]
        miembros.extend(list(self.set_miembros.all().filter(rol__isnull=False)))

        return miembros



    def get_miembro(self, usuario):
        """
        Metodo que devuelve el usuario perteneciente a un proyecto
        Parametros:
            usuario: Usuarios
       Return
            miembro: usuario
        """
        if self.scrumMaster.id == usuario.id:
            return self.miembro_set.get(usuario=usuario)
        else:
            if self.miembro_set.filter(usuario=usuario).exists():
                return self.miembro_set.get(usuario=usuario)
            else:
                return None


    def get_miembros(self):
        """
        Metodo para obtener los miembros de un proyecto
        Retorna:
            QuerySet: objeto con todos los participantes del Proyecto.
        """
        miembros = [self.miembro_set.get(usuario=self.scrumMaster)]
        miembros.extend(list(self.miembro_set.all().filter(rol__isnull=False)))

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


class Miembro(models.Model):
    """
    Modelo que representa la relacion entre un usuario del sistema y un proyecto en particular.
    Atributos:
        - proyecto: Proyecto
        - usuario: Usuario
        - rol: RolesDeSistema
    """
    proyecto = models.ForeignKey('Proyectos.Proyecto', on_delete=models.CASCADE,null=True)
    usuario = models.ForeignKey('Usuarios.Usuario', on_delete=models.CASCADE,null=True)
    rol = models.ForeignKey('permisos.RolesdeSistema', on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.usuario.get_full_name()


    def get_id_proyecto (self):
        return self.proyecto.id_proyecto

    
    
    def get_rol_nombre(self):
        """

        """
        if self.rol is not None:
            return self.rol.nombre
        else:
            return 'Scrum Master' if self.usuario == self.proyecto.scrumMaster else None

    
    