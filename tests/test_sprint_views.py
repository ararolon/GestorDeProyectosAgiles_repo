from django.test import TestCase
from django.urls import reverse,Client
from Sprint.views import *
from Proyectos.models import Proyecto

"""
test para los views.py de Sprint
"""
 
class Test_sprint_views(TestCase):
    def setUp(self):
        self.client = Client()
        self.proyecto = Proyecto.objects.create(nombre='test',descripcion='prueba')
        self.proyecto.save()
        
    def test_crear_Sprint(self):
        path = reverse('crearSprint',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/crearSprint.html')
 
    def test_mostrar_sprint(self):
        path = reverse('mostrarSprint')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sprint/mostrarSprint.html')   