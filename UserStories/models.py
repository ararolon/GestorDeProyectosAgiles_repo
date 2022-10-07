from email.policy import default
from pydoc import describe
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.postgres.fields import ArrayField
from Usuarios.models import Usuario
from django.core.validators import MaxValueValidator, MinValueValidator




# Create your models here.

class Estados_Kanban(models.Model):
   """
    Modelo que representa los estados del tablero kanban,
    se relaciona con los tipos de User stories
   
    clase Padre:
      models.Model
   """

   nombre = models.CharField(max_length=20,blank=False,unique=True)
   defecto = models.BooleanField(default=False)

   class Meta:
        verbose_name = 'Estado_Kanban'
        verbose_name_plural = 'Estados_Kanban'
   
   def __str__(self):
      return self.nombre


#preguntar si un user story es por proyecto tambien
class TipoUSerStory(models.Model):

  """
        Modelo que representa los tipos de user stories en el sistema
    
        Clase Padre : models.Model
  """
  nombre = models.CharField(max_length=20,unique=True,blank=False)
  descripcion = models.TextField(max_length=80,blank=True,null=True)
  estados_kanban = models.ManyToManyField(Estados_Kanban)
  class Meta:
        verbose_name = 'TipoUS'
        verbose_name_plural = 'TiposUS'
     
  def __str__(self):
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
  id_proyecto = models.IntegerField(null=True)
  nombre = models.CharField(max_length=20,unique=True,blank=False)  
  descripcion = models.TextField(max_length=60,blank=True)
  tipo = models.ForeignKey(TipoUSerStory,on_delete=models.CASCADE, null=True)
  prioridad = models.CharField(max_length=20,choices=PRIORIDAD_CHOICES,blank=False)
  miembro_asignado = models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True)
  comentarios = models.TextField(default='',blank=True)
  horas_estimadas = models.IntegerField(default=0,blank=False,validators=[MaxValueValidator(100), MinValueValidator(1)])
  #id_proyecto = models.ForeignKey(Proyecto,on_delete=models.CASCADE,blank=False)
  #guarda el id del proyecto al que pertenece para filtrar por proyecto
  class Meta:
    verbose_name = 'UserStory'
    verbose_name_plural = 'UserStories'
     
  def __str__(self):
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


  def es_usado(self,id):
    """
    Funcion que determina si el tipo de US
    esta asociado a algun User story

    Argumento:
          self: objeto UserStory
          id : id del Tipo de US a ser analizado 
        
    Retorna:
         True si esta siendo usado , False en caso contrario

    """
    t = TipoUSerStory.objects.get(id=id)
    if UserStories.objects.filter(tipo=t).exists():
       return True

    return False    









  