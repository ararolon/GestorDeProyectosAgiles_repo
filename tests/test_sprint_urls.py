import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from Sprint.views import crearSprint, mostrarSprint
"""
test para los urls del Sprint
"""
class Test_sprint_urls(TestCase):
 
   #  def test_crearSprint(self):
   #     url = reverse('crearSprint', args=[self.proyecto.id])
   #     self.assertEqual(resolve(url).func, crearSprint, "no se pudo crear sprint")

    def test_mostrarSprint(self):
       url = reverse('mostrarSprint')
       self.assertEqual(resolve(url).func, mostrarSprint, "no se pudo crear sprint")
