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


  
   