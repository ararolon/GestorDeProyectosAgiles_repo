from django.db import models
from django.contrib.auth.models import Permission
"""
RF100: EL sistema cuenta con una lista de roles por defecto iniciales:
- Superusuario/administrador del sistema.
- Usuario del sistema.
- Scrum Master.
- Product owner.
- Cliente.
- Desarrollador back-end.
- Desarrollador front-end.
- Tester.
- DBA.
"""
# Create your models here.
class RolesdeSistema(models.Model):
    """
    Modelo para roles del sistema
    obs: Los roles del sistema no pueden ser eliminados
    clase padre : models.Model
    Atributo:
    nombre = nombre del rol
    descripcion =  descripcion breve del rol del sistema
    permisos = conjunto de permisos para el rol
    """
    nombre = models.CharField(max_length=20, blank=False, unique=True)
    descripcion = models.TextField(max_length=60, blank=True)
    permisos = models.ManyToManyField(Permission, blank=True)  # Indica que varios roles pueden tener varios permisos
    
    class Meta:
        permissions = [
            ('crear_usuario', 'Crear usuario'),
            ('eliminar_usuario', 'Eliminar usuario'),
            ('acceder_al_sistema','Acceder al sistema'),
            ('crear_roles', 'Crear roles'),
            ('asignar_roles', 'Asignar roles a usuario'),
            ('visualizar_usuario', 'Visualizar usuario del Sistema'),            
            ('crear_proyecto', 'Crear Proyecto'),
            ('editar_proyecto', 'Editar Proyecto'),
            ('visualizar_proyecto', 'Visualizar Proyecto'),
            ('cancelar_proyecto', 'Cancelar Proyecto'),
            ('eliminar_miembros', 'Eliminar miembros de un proyecto'),
            ('visualizar_historial_proyecto', 'Visualizar historial del proyecto'),
            ('modificar_fecha', 'Modificar fecha de inicio y fin del proyecto'),
            ('modificar_estado_proyecto', 'Modificar estado del proyecto'),
            ('crear_sprint', 'Crear sprint'),
            ('modificar_sprint', 'Modificar sprint'),
            ('modificar_estado_sprint', 'Modificar estado de un sprint'),
            ('crear_us','Crear US'),
            ('modificar_us','Modificar US'),
            ('modificar_estado_us','Modificar estado de US'),
            ('cancelar_us','Cancelar US'),
            ('consultar_historial_us','Consultar historial de un US'),
            ('modificar_backlog','Modificar Product Backlog'),
            ('modificar_sprint_backlog','Modificar Sprint Backlog'),
            ('crear_tipos_us','Crear tipos de US'),
            ('modificar_tipos_us','Modificar tipos de US'),
            ('visualizar_burndown_chart','Visualizar Burndown Chart'),
            ('visualizar_kanban','Visualizar Tabla Kamban'),
        ]    

    def _str_(self):
        return self.nombre

    def get_permisos(self):
        """
        Método que retorna los permisos asignados al rol.
        :return: lista de permisos
        """
        return [p for p in self.permisos.all()]

    def asignar_permisos(self):

        per1 = Permission.objects.get(codename='crear_proyecto')

        Rol = RolesdeSistema.objects.create()

        rol.
