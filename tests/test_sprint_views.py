from importlib.resources import path
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
        self.sprint = Sprint.objects.create(nombre_sprint='testSprint', descripcion='testSprint', id_proyecto=self.proyecto.id,id_sprint='1')
        self.US =  UserStories.objects.create(nombre='test',horas_estimadas=10)
        self.sprint.historias.add(self.US)
        self.sprint.save()

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
 
    def test_iniciarSprint(self):
        path = reverse('iniciarSprint', args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)

    # def test_cancelarSprint(self):
    #     path = reverse('cancelarSprint')
    #     response = self.client.post(path,data={'id_sprint': '1'})
    #     self.assertEqual(response.status_code, 302)
    
    def test_asignar_us(self):
        path = reverse('asignarUS',args=[self.US.nombre,self.sprint.id])
        response = self.client.get(path)
        self.assertTemplateNotUsed(response,'Sprint/asignarUS.html',"No se encontro el template")

    def test_sprint_backlog(self):
        path =reverse('sprintbacklog',args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/sprintbacklog.html')

    def test_modificarSprint(self):
        path = reverse('modificarSprint',args=[self.proyecto.id,self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/modificarSprint.html')
    
    def test_asignarMiembroSprint(self):
        path = reverse('asignarMiembroSprint',args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200,"Error")
        self.assertTemplateUsed(response, 'Sprint/asignarMiembroSprint.html')

    def test_index_asignar(self):
        path = reverse('indexasignar',args=[self.sprint.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code,200,"Error")
        self.assertTemplateUsed(response,'Sprint/asignarUS.html',"No se encontro el template")
   
    def test_quitar_us(self):
        path = reverse('desasignar',args=[self.US.nombre,self.sprint.id])
        response = self.client.get(path)
        self.assertTemplateNotUsed(response,'Sprint/asignarUS.html',"No se encontro el template")

    # def test_asignarHistoria(self):
    #     path = reverse('sprintbacklog',args=[self.sprint.id])
    #     response = self.client.post(path,data={'user_id': 'testUS'})
    #     self.assertEqual(response.status_code, 302)