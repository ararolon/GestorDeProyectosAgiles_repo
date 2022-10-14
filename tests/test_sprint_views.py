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
        self.proyecto = Proyecto.objects.create(nombre='test',id_proyecto='1',descripcion='prueba')
        self.sprint = Sprint.objects.create(nombre_sprint='testSprint', descripcion='testSprint', id_proyecto=self.proyecto.id)
    
    def test_crear_Sprint(self):
        path = reverse('crearSprint',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/crearSprint.html')
    
    def test_listar_Sprint(self):
        path = reverse('listarSprint',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/listarSprint.html')
 
    def test_mostrar_sprint(self):
        path = reverse('mostrarSprint')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Sprint/mostrarSprint.html')   

    def test_iniciarSprint(self):
        path = reverse('iniciarSprint', args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)

    def test_cancelarSprint(self):
        path = reverse('cancelarSprint', args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
    

    def test_asignar_us(self):
        path = reverse('asignarUS',args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/asignarUS.html')

    def test_sprint_backlog(self):
        path =reverse('sprintbacklog',args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/sprintbacklog.html')
    
