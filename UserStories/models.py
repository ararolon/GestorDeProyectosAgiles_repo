from multiprocessing.dummy import Array
from pydoc import describe
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.postgres.fields import ArrayField
from Usuarios.models import Usuario



# Create your models here.

class Estados_Kanban(models.Model):
   """
    Modelo que representa los estados del tablero kanban,
    se relaciona con los tipos de User stories
   
    clase Padre:
      models.Model
   """

   nombre = models.CharField(max_length=20,blank=False,unique=True)

   class Meta:
        verbose_name = 'Estado_Kanban'
        verbose_name_plural = 'Estados_Kanban'
   
   def _str_(self):
      return self.nombre


#preguntar si un user story es por proyecto tambien
class TipoUSerStory(models.Model):

  """
        Modelo que representa los tipos de user stories en el sistema
    
        Clase Padre : models.Model
  """
  nombre = models.CharField(max_length=20,unique=True,blank=False)
  descripcion = models.TextField(max_length=80,blank=True)
  estados_kanban = ArrayField(models.CharField(max_length=20,blank=False))
  class Meta:
        verbose_name = 'TipoUS'
        verbose_name_plural = 'TiposUS'
     
  def _str_(self):
      return self.nombre
     

  def get_estados_kanban(self):
    """
     Funcion que devuelve los estados del kanban que tiene asignado
     un tipo de US
    """
   
    return [e for e in self.estados_kanban.all()]



"""
 Prioridades de User stories
"""

PRIORIDAD_CHOICES=[
    ('ALTA','Alta'),
    ('MEDIA','Media'),
    ('BAJA','Baja'),
]

class UserStories(models.Model):
  """
    Modelo que representa a los user stories de un proyecto

    Clase Padre : models.Model
  """
  id_us = models.AutoField(primary_key = True)
  nombre = models.CharField(max_length=20,unique=True,blank=False)  
  descripcion = models.TextField(max_length=60,blank=True)
  tipo = models.ForeignKey(TipoUSerStory,on_delete=models.CASCADE,null=False,blank=False)
  prioridad = models.CharField(max_length=20,choices=PRIORIDAD_CHOICES,blank=False)
  miembro_asignado = models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True)
  comentarios = models.TextField(default='',blank=True)
  horas_estimadas = models.IntegerField(default=0,blank=False)
  #id_proyecto = models.ForeignKey(Proyecto,on_delete=models.CASCADE,blank=False)
  #guarda el id del proyecto al que pertenece para filtrar por proyecto
  class Meta:
    verbose_name = 'UserStory'
    verbose_name_plural = 'UserStories'
     
  def _str_(self):
    return self.nombre

  def get_miembro_asignado(self):
    """
    Funcion que obtiene el miembro asignado al user story

      Argumento :
           Objeto User Story

      Retorna : 
           El miembro del equipo asignado  
    """
    return self.miembro_asignado








  