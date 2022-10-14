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
      self.proyecto = Proyecto.objects.create(nombre='testProyecto', id_proyecto='1', descripcion='testProyecto')
      self.sprint = Sprint.objects.create(nombre_sprint='testSprint', descripcion='testSprint')

   def test_crearSprint(self):
      url = reverse('crearSprint', args=[self.proyecto.id])
      self.assertEqual(resolve(url).func, crearSprint, "no se pudo crear sprint")

   def test_mostrarSprint(self):
      url = reverse('mostrarSprint')
      self.assertEqual(resolve(url).func, mostrarSprint, "no se pudo mostrar sprint")
   
   def test_listarSprint(self):
      url = reverse('listarSprint',args=[self.proyecto.id])
      self.assertEqual(resolve(url).func, listarSprint, "no se pudo mostrar sprint")

   def test_iniciarSprint(self):
      url = reverse('iniciarSprint', args=[self.sprint.id])
      self.assertEqual(resolve(url).func, iniciarSprint, "no se pudo iniciar sprint")

   def test_cancelarSprint(self):
      url = reverse('cancelarSprint', args=[self.sprint.id])
      self.assertEqual(resolve(url).func, cancelarSprint, "no se pudo cancelar sprint")
   
   def test_asignarUS(self):
      url = reverse('asignarUS', args=[self.sprint.id])
      self.assertEqual(resolve(url).func,asignar_us, "no se pudo asignar US")

   def test_sprintbacklog(self):
      url = reverse('sprintbacklog', args=[self.sprint.id])
      self.assertEqual(resolve(url).func,ver_sprintbacklog, "no se pudo ver el sprint backlog")