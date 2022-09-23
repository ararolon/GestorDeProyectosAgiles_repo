from nntplib import GroupInfo
from unicodedata import name
from django.db import models
from django.contrib.auth.models import Permission, Group



# Create your models here.
class RolesdeSistema(models.Model):
    
    nombre = models.CharField(max_length=20, blank=False, unique=True)
    defecto = models.BooleanField(default=False) # indica si el rol creado es predeterminado en el sistema y no puede borrarse.
    descripcion = models.TextField(max_length=60, blank=True)
    permisos = models.ManyToManyField(Permission, blank=True)  # Indica que varios roles pueden tener varios permisos
   # rol_usuario = models.ManyToManyField(RolUsuario, blank=True)

    class Meta:
        permissions = [
            ('_crear_usuario', 'Crear usuario'),
            ('_eliminar_usuario', 'Eliminar usuario'),
            ('_acceder_al_sistema','Acceder al sistema'),
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
            ('_iniciar_proyecto','Iniciar un proyecto'),
            ('_asignar_us','Asignar US'),
        ]    

    def __str__(self):
      return self.nombre

    def get_permisos(self):
      """
      Método que retorna los permisos asignados al rol.
      :return: lista de permisos
      """
      return [p for p in self.permisos.all()]

    def get_nombre(self):
      return self.nombre    

    
    def darpermisos_a_grupo(self,grupo):

      """
      Funcion que asigna todos los permisos dados a un rol a un grupo relacionado a rol
      param: el rol con los permisos
      param: el grupo al que se le quiere dar los permisos
      """

      permisos = self.get_permisos()
        
      for p in permisos:
        grupo.permissions.add(p)



    def es_utilizado(self):

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
