from multiprocessing.dummy import Array
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Estados_Kanban(models.Model):
   """
    Modelo que representa los estados del tablero kanban,
    se relaciona con los tipos de User stories
   
    clase Padre:
      models.Model
   """

   nombre = models.CharField(max_length=20,blank=False)

   class Meta:
        verbose_name = 'Estado_Kanban'
        verbose_name_plural = 'Estados_Kanban'
   
   def _str_(self):
      return self.nombre



class TipoUSerStory(models.Model):

  """
        Modelo que representa los tipos de user stories en el sistema
    
        Clase Padre : models.Model
  """
  nombre = models.CharField(max_length=20,unique=True,blank=False)
  prefijo = models.CharField(max_length=20)
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




