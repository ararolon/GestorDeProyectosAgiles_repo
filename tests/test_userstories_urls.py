from nturl2path import url2pathname
import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from Proyectos.models import Proyecto
from UserStories.views import *

"""
Tests de urls de UserStories
"""


class Test_urls(TestCase):

  def setUp(self):

    self.proyecto = Proyecto.objects.create(nombre='prueba',descripcion='prueba proyecto')
    self.proyecto.save()
    self.estado = Estados_Kanban.objects.create(nombre='prueba')
    self.us = UserStories.objects.create(id_proyecto=self.proyecto.id,nombre='prueba')

 

  def test_crearEstado(self):
    url = reverse('crear_estado',args=[self.proyecto.id] )
    self.assertEqual(resolve(url).func, crear_estadokanban, "no se pudo dirigir a el url de crear_estadoKanban")

  def test_crearTipoUS(self):
    url = reverse('crear_tipoUS', args=[self.proyecto.id])
    self.assertEqual(resolve(url).func, crear_TipoUS,"no se pudo dirigir a el url de crear_tipoUS")

  def test_crearUS(self):
    url = reverse('crear_us',args=[self.proyecto.id])
    self.assertEqual(resolve(url).func, crear_us,"no se pudo dirigir a el url de crear_us")
  
  def test_importarTipoUS(self):
    url = reverse('importar_tipoUS', args=[self.proyecto.id])
    self.assertEqual(resolve(url).func, importar_tipoUS,"no se pudo dirigir a el url de importar_tipoUS")
   
  def test_tabla_kanban(self):
    url = reverse('tabla_kanban', args=[self.proyecto.id])
    self.assertEqual(resolve(url).func, tablaKanban,"no se pudo dirigir a el url de tabla_kanban")
   
  def test_cambiarEstado(self):
    url = reverse('cambiarEstado', args=[self.us.id_us, self.estado.id]) 
    self.assertEqual(resolve(url).func, cambiarEstado,"no se pudo dirigir a el url de cambiarEstado")