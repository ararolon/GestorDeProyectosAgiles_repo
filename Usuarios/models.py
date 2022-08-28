from asyncore import file_dispatcher
from audioop import add
from unicodedata import name
from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Permission, Group
from django.db import models

from Permisos.models import RolesdeSistema



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
        per1 = Permission.objects.get(codename='crear_usuario')
        per2 = Permission.objects.get(codename='eliminar_usuario')
        per3 = Permission.objects.get(codename='crear_proyecto')
        per4 = Permission.objects.get(codename='asignar_roles')
        per5 = Permission.objects.get(codename='visualizar_usuario')
        per6 = Permission.objects.get(codename='crear_roles')

        grupo = Group.objects.get(name='administrador')
        grupo.permissions.add(per1,per2,per3,per4,per5,per6)
        
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