from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse
from Proyectos.views import *

"""
test para los views.py de Proyectos
"""

class Test_proyecto_views(TestCase):

    def test_crear_Proyecto(self):
        path = reverse('crearProyecto')
        response = self.client.get(path)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/crearProyectos.html')

    def test_mostrar_proyecto(self):
        path = reverse('mostrarUnProyecto')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/mostrarUnProyecto.html')

    def test_listar_proyectos(self):
        path = reverse('listarProyectos')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/listarProyectos.html')
