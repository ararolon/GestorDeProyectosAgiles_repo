import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from Proyectos.models import Proyecto
from Proyectos.views import crearProyecto
from Proyectos.views import listarProyectosUser
from Proyectos.views import listarProyectos
from Proyectos.views import asignar_miembro
from Proyectos.views import mostrarProyecto
from Proyectos.views import importarRol
from Proyectos.views import asignarRol
from Proyectos.views import iniciarProyecto
from Proyectos.views import cancelarProyecto
from Usuarios.models import Usuario
from Proyectos.views import mostrarProyectoAdmin



"""
test para los urls del Proyecto
"""
class Test_proyecto_urls(TestCase):

    def setUp(self):
        self.proyecto = Proyecto.objects.create(nombre='testProyecto', descripcion='testProyecto')
        self.miembro = Usuario.objects.create(first_name='testMiembro', username='testMiembro')

    def test_crearProyecto(self):
        url = reverse('crearProyecto')
        self.assertEqual(resolve(url).func, crearProyecto, "no se pudo crear proyecto")

    def test_listarProyectosUser(self):
        url = reverse('listarProyectosUser')
        self.assertEqual(resolve(url).func, listarProyectosUser)

    def test_listarProyectos(self):
        url = reverse('listarProyectos')
        self.assertEqual(resolve(url).func, listarProyectos)

    def test_asignar_miembro(self):
        url = reverse('asignar_miembro', args=[self.proyecto.id])
        self.assertEqual(resolve(url).func, asignar_miembro)

    def test_asignarRol(self):
        url = reverse('asignarRol', args=[self.proyecto.id, self.miembro.id])
        self.assertEqual(resolve(url).func, asignarRol)

    def test_mostrarProyecto(self):
        url = reverse('mostrarProyecto', args=[self.proyecto.id])
        self.assertEqual(resolve(url).func, mostrarProyecto)

    def test_importarRol(self):
        url = reverse('importarRol', args=[self.proyecto.id])
        self.assertEqual(resolve(url).func, importarRol)

    def test_iniciarProyecto(self):
        url = reverse('iniciarProyecto', args=[self.proyecto.id])
        self.assertEqual(resolve(url).func, iniciarProyecto)

    def test_cancelarProyecto(self):
        url = reverse('cancelarProyecto', args=[self.proyecto.id])
        self.assertEqual(resolve(url).func, cancelarProyecto)    
    
    def test_mostrarProyectoAdmin(self):
        url = reverse('mostrarProyectoAdmin', args=[self.proyecto.id])
        self.assertEqual(resolve(url).func, mostrarProyectoAdmin)