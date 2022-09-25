import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from Sprint.views import *
from Proyectos.models import Proyecto
from Sprint.models import Sprint

"""
test para los urls del Sprint
"""
class Test_sprint_urls(TestCase):

   def setUp(self):
      self.proyecto = Proyecto.objects.create(nombre='testProyecto', descripcion='testProyecto')
      self.sprint = Sprint.objects.create(nombre_sprint='testSprint',fecha_inicio='2022-10-01',fecha_fin='2022-10-15', descripcion='testSprint')

   def test_crearSprint(self):
      url = reverse('crearSprint', args=[self.proyecto.id])
      self.assertEqual(resolve(url).func, crearSprint, "no se pudo crear sprint")

   def test_mostrarSprint(self):
      url = reverse('mostrarSprint')
      self.assertEqual(resolve(url).func, mostrarSprint, "no se pudo mostrar sprint")

   def test_iniciarSprint(self):
      url = reverse('iniciarSprint', args=[self.sprint.id])
      self.assertEqual(resolve(url).func, iniciarSprint, "no se pudo iniciar sprint")

   def test_cancelarSprint(self):
      url = reverse('cancelarSprint', args=[self.sprint.id])
      self.assertEqual(resolve(url).func, cancelarSprint, "no se pudo cancelar sprint")