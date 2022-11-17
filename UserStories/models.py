from email.policy import default
from hashlib import blake2b
from pydoc import describe
from pyexpat import model
from statistics import mode
from sys import maxsize
from unittest.util import _MAX_LENGTH
from wsgiref.validate import validator
from django.db import models
from django.contrib.postgres.fields import ArrayField
from  Usuarios.models   import Usuario,Notificaciones
from django.core.validators import MaxValueValidator, MinValueValidator
from Sprint.models import *
from simple_history.models import HistoricalRecords



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
  miembro_asignado = models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True)
  comentarios = models.TextField(default='',blank=True)
  #esfuerzo en horas , se puede dejar en blanco pero es necesario para que entre en algun sprint
  horas_estimadas = models.IntegerField(default=0,blank=True,validators=[MaxValueValidator(100), MinValueValidator(0)], null=True)
  #Prioridad de negocio , valores del 1 al 10
  PN = models.IntegerField(validators = [MaxValueValidator(10),MinValueValidator(1)],blank=False,default = 0)
  #Prioridad tecnica , valores de 1 al 10
  PT = models.IntegerField(validators = [MaxValueValidator(10),MinValueValidator(1)],blank = False,default = 0)
  #Peso asignado si ya fue trabajado anteriormente en un sprint, PS =3 si ya fue trabajado , PS = 0 si todavia no estuvo en un Sprint
  PS = models.IntegerField(default =0, blank =True)
  #variable prioridad final , resultante del calculo de la formula : ( ( 0,6 x PN + 0,4 x PT )  + PS
  estado = models.ForeignKey(Estados_Kanban,on_delete=models.CASCADE,null=True,blank=True)
  Prioridad = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True)
  motivo_cancelacion = models.TextField(max_length=60,blank=True)
  en_sprint = models.BooleanField(default=False)
  horas_trabajadas = models.IntegerField(default=0,blank=True,validators=[MaxValueValidator(100), MinValueValidator(0)], null=True)
  history = HistoricalRecords()
  actividad = models.CharField(max_length=50, blank=True, null=True)
  horas = models.IntegerField(default=0,blank=True)
  
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











  