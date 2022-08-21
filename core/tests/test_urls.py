import pytest
"""
Tests de las vistas de SS0
"""

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from SSO.views import configuraciones_iniciales, home

class Test_urls(SimpleTestCase):

   def test_home(self):
     url = reverse('home')
     self.assertEqual(resolve(url).func,home)

   def test_configuraciones_iniciales(self):
       url = reverse('confinicial')
       self.assertEqual(resolve(url).func,configuraciones_iniciales)

   #generando un error
   def test_error_home(self):
       url = reverse('home')
       self.assertEqual(resolve(url).func, configuraciones_iniciales)