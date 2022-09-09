from audioop import add
from unicodedata import name
from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Permission, Group
from django.db import models

from permisos.models import RolesdeSistema



# Create your models here.


class Usuario(User):
    """
        Modelo utilizado para obtener los usuarios del sistema
        el modelo extiende del modelo User de Django
        modelo proxy
        Modelo padre : django.contrib.auth.models User
    """

    class Meta:
        proxy = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name
 

    def es_administrador(self):
        """
         Pregunta si el usuario es el administrador del sistema

         :return: Booleano , True si es el administrador , False si no lo es
        """
        return self.groups.filter(name='administrador').exists()

 
    def dar_permisos_administrador(self):
        
        """
         Funcion para asignar los permisos para el administrador del sistema
         la primera vez que accede al sistema.
        """
        per1 = Permission.objects.get(codename='_crear_usuario')
        per2 = Permission.objects.get(codename='_eliminar_usuario')
        per3 = Permission.objects.get(codename='_crear_proyecto')
        per4 = Permission.objects.get(codename='_asignar_roles')
        per5 = Permission.objects.get(codename='_visualizar_usuario')
        per6 = Permission.objects.get(codename='_crear_roles')

        rol = RolesdeSistema.objects.get(nombre='administrador')
        rol.permisos.add(per1,per2,per3,per4,per5,per6)

        grupo = Group.objects.get(name='administrador')
        permisos = rol.get_permisos() # obtiene todos los permisos del rol y los guarda en una variable 
        for p in permisos: #itera la variable y va guardando todos los permisos del rol dentro del grupo
            grupo.permissions.add(p)
        
        self.groups.add(grupo) 


    def tiene_permiso(self,permiso):
        """
          Funcion que retorn un booleano si es que el permiso esta siendo usado

         :param: self object
         :param: Permission object
        """   

        if self.has_perm(permiso):
            flag = True
        else:
            flag = False    

        return flag

    #asigna un solo rol
    def asignar_rol_a_usuario(self,rol_id):
        """
        Funcion para asignar un rol a un usuario del sistema
        
        :param1: el usuario al que sera aignado el permiso 
        :param2: el id del rol.
        """
        rol = RolesdeSistema.objects.get(id=rol_id)
        group = Group.objects.get(name=rol.nombre)
        self.groups.add(group)
   
    #asignar varios roles
    def asignar_roles_usuarios(self,roles):
          
     """
     Funcion para asignar varios roles a un usuario
     """
     
     for r in roles:
        rol = RolesdeSistema.objects.get(id=r)
        group = Group.objects.get(name=rol.nombre)
        self.groups.add(group)
       

    def desasignar_rol(self,rol_id):
        """
         Funcion que permite quitar un rol a un usuario
        """

        rol = RolesdeSistema.objects.get(id = rol_id)
        grupo = Group.objects.get(name = rol.nombre)
        self.groups.remove(grupo)
        

       
          






