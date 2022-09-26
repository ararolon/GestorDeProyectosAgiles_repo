from django.test import TestCase
from django.urls import reverse
from Sprint.views import *
from Proyectos.models import Proyecto
from Sprint.models import Sprint

"""
test para los views.py de Sprint
"""
 
class Test_sprint_views(TestCase):
    def setUp(self):
        self.proyecto = Proyecto.objects.create(nombre='test',descripcion='prueba')
        self.sprint = Sprint.objects.create(nombre_sprint='testSprint',fecha_inicio='2022-10-01',fecha_fin='2022-10-15', descripcion='testSprint')
    
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

    def test_iniciarSprint(self):
        print(self.sprint.estado_sprint)
        path = reverse('iniciarSprint', args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)

    def test_cancelarSprint(self):
        path = reverse('cancelarSprint', args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
