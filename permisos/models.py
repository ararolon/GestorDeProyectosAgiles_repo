from nntplib import GroupInfo
from unicodedata import name
from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class RolesdeSistema(models.Model):
    
    nombre = models.CharField(max_length=20, blank=False, unique=True)
    defecto = models.BooleanField(default=False) # indica si el rol creado es predeterminado en el sistema y no puede borrarse.
    descripcion = models.TextField(max_length=60, blank=True)
    permisos = models.ManyToManyField(Permission, blank=True)  # Indica que varios roles pueden tener varios permisos
    
    class Meta:
        permissions = [
            ('_crear_usuario', 'Crear usuario'),
            ('_eliminar_usuario', 'Eliminar usuario'),
            ('_acceder_sistema','Acceder al sistema'),
            ('_crear_roles', 'Crear roles'),
            ('_asignar_roles', 'Asignar roles a usuario'),
            ('_visualizar_roles', 'Visualizar roles a usuario'),
            ('_eliminar_roles', 'Eliminar roles a usuario'),
            ('_visualizar_usuario', 'Visualizar usuario del Sistema'),            
            ('_crear_proyecto', 'Crear Proyecto'),
            ('_editar_proyecto', 'Editar Proyecto'),
            ('_visualizar_proyecto', 'Visualizar Proyecto'),
            ('_cancelar_proyecto', 'Cancelar Proyecto'),
            ('_eliminar_miembros', 'Eliminar miembros de un proyecto'),
            ('_visualizar_historial_proyecto', 'Visualizar historial del proyecto'),
            ('_modificar_fecha', 'Modificar fecha de inicio y fin del proyecto'),
            ('_modificar_estado_proyecto', 'Modificar estado del proyecto'),
            ('_crear_sprint', 'Crear sprint'),
            ('_modificar_sprint', 'Modificar sprint'),
            ('_modificar_estado_sprint', 'Modificar estado de un sprint'),
            ('_crear_us','Crear US'),
            ('_modificar_us','Modificar US'),
            ('_modificar_estado_us','Modificar estado de US'),
            ('_cancelar_us','Cancelar US'),
            ('_consultar_historial_us','Consultar historial de un US'),
            ('_modificar_backlog','Modificar Product Backlog'),
            ('_modificar_sprint_backlog','Modificar Sprint Backlog'),
            ('_crear_tipos_us','Crear tipos de US'),
            ('_modificar_tipos_us','Modificar tipos de US'),
            ('_visualizar_burndown_chart','Visualizar Burndown Chart'),
            ('_visualizar_kanban','Visualizar Tabla Kamban'),
        ]    

    def _str_(self):
        return self.nombre

    def get_permisos(self):
        """
        Método que retorna los permisos asignados al rol.
        :return: lista de permisos
        """
        return [p for p in self.permisos.all()]

"""
class Permiso(models.Model):
    
    def get_permisos_clean(self):
        
        #Metodo que colecta los permisos activos
        #:return: una lista de permisos activos
        
        permisos = []
        permisos = permisos + (['Crear usuario'] if self.crear_usuario else [])
        permisos = permisos + (['Eliminar usuario'] if self.eliminar_usuario else [])
        permisos = permisos + (['Crear roles'] if self.crear_roles else [])
        permisos = permisos + (['Asignar roles a usuario'] if self.asignar_roles else [])
        permisos = permisos + (['Visualizar usuario del Sistema'] if self.visualizar_usuario else [])
        permisos = permisos + (['Crear Proyecto'] if self.crear_proyecto else [])
        permisos = permisos + (['Editar Proyecto'] if self.editar_proyecto else [])
        permisos = permisos + (['Visualizar Proyecto'] if self.visualizar_proyecto else [])
        permisos = permisos + (['Cancelar Proyecto'] if self.cancelar_proyecto else [])
        permisos = permisos + (['Eliminar miembros de un proyecto'] if self.eliminar_miembros else [])
        permisos = permisos + (['Visualizar historial del proyecto'] if self.visualizar_historial_proyecto else [])
        permisos = permisos + (['Modificar fecha de inicio del proyecto'] if self.modificar_fecha_ini else [])
        permisos = permisos + (['Modificar fecha de finalizacion del proyecto'] if self.modificar_fecha_fin else [])
        permisos = permisos + (['Modificar estado del proyecto'] if self.modificar_estado_proyecto else [])
        permisos = permisos + (['Crear sprint'] if self.crear_sprint else [])
        permisos = permisos + (['Modificar sprint'] if self.modificar_sprint else [])
        permisos = permisos + (['Modificar estado de un sprint'] if self.modificar_estado_sprint else [])
        permisos = permisos + (['Crear US'] if self.crear_us else [])
        permisos = permisos + (['Modificar US'] if self.modificar_us else [])
        permisos = permisos + (['Modificar estado de US'] if self.modificar_estado_us else [])
        permisos = permisos + (['Cancelar us'] if self.cancelar_us else [])
        permisos = permisos + (['Consultar historial de un US'] if self.cosultar_historial_us else [])
        permisos = permisos + (['Modificar Product Backlog'] if self.modificar_backlog else [])
        permisos = permisos + (['Modificar Sprint Backlog'] if self.modificar_sprint_backlog else [])
        permisos = permisos + (['Crear tipos de US'] if self.crear_tipos_us else [])
        permisos = permisos + (['Modificar tipos de US'] if self.modificar_tipos_us else [])
        permisos = permisos + (['Visualizar Burndown Chart'] if self.visualizar_burndown_chart else [])
        permisos = permisos + (['Visualizar Visualizar Tabla Kanban'] if self.visualizar_kanban else [])

      """
      Funcion que verifica si un rol esta siendo utilizado

      :return: Booleano ,True si esta siendo utilizado, False caso contrario
      """
      #Busca el grupo por nombre de rol
      if not Group.objects.exists():
        grupo = Group.objects.create(name = self.nombre)

      else:                
        grupo = Group.objects.get(name= self.nombre)
    
      return grupo.user__set.all().exists() if grupo is not None else False
   
    


