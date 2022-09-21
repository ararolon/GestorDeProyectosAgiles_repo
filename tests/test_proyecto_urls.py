import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from Proyectos.views import crearProyecto
from Proyectos.views import listarProyectosUser
from Proyectos.views import listarProyectos

"""
test para los urls del Proyecto
"""
class Test_proyecto_urls(TestCase):

    def test_crearProyecto(self):
        url = reverse('crearProyecto')
        self.assertEqual(resolve(url).func, crearProyecto, "no se pudo crear proyecto")

    def test_listarProyectosUser(self):
        url = reverse('listarProyectosUser')
        self.assertEqual(resolve(url).func, listarProyectosUser)

    def test_listarProyectos(self):
        url = reverse('listarProyectos')
        self.assertEqual(resolve(url).func, listarProyectos)