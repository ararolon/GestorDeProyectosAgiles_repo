from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse
from Proyectos.views import *

"""
test para los views.py de Proyectos
"""

class Test_proyecto_views(TestCase):

    def setUp(self):
        self.scrum_master = Usuario.objects.create_user(first_name='scrum_master', username='scrum_master')
        self.proyecto = Proyecto.objects.create(nombre='testProyecto', descripcion='testProyecto', scrumMaster=self.scrum_master)
        self.miembro = Usuario.objects.create(first_name='testMiembro', username='testMiembro')

    def test_crear_Proyecto(self):
        path = reverse('crearProyecto')
        response = self.client.get(path)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/crearProyectos.html')

    def test_mostrar_proyecto(self):
        path = reverse('listarProyectosUser')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/listarProyectosUser.html')

    def test_listar_proyectos(self):
        path = reverse('listarProyectos')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/listarProyectos.html')

    def test_asignar_miembro(self):
        path = reverse('asignar_miembro', args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/asignar_miembro.html')

    def test_mostrarProyecto(self):
        path = reverse('mostrarProyecto', args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/mostrarProyecto.html')

    def test_mostrarProyectoAdmin(self):
        path = reverse('mostrarProyectoAdmin', args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/mostrarProyectoAdmin.html')

    def test_importarRol(self):
        path = reverse('importarRol', args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/importarRol.html')

    def test_asignarRol(self):
        path = reverse('asignarRol', args=[self.proyecto.id, self.miembro.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyectos/asignarRol.html')

    def test_iniciarProyecto(self):
        print(self.proyecto.estado)
        path = reverse('iniciarProyecto', args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        # 302 found porque se redirige a la página de mostrarProyecto

    def test_cancelarProyecto(self):
        path = reverse('cancelarProyecto', args=[self.proyecto.id])
        # pass motivo as a post data
        response = self.client.post(path,data={'motivo': 'test'})
        self.assertEqual(response.status_code, 302)
        # 302 found porque se redirige a la página de mostrarProyecto

    def test_visualizar_historial(self):
        path = reverse('historial', args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code,200)

    def test_finalizarProyecto(self):
        path = reverse('finalizarProyecto', args=[self.proyecto.id])
        # pass motivo as a post data
        response = self.client.post(path)
        self.assertEqual(response.status_code, 302)
        # 302 found porque se redirige a la página de mostrarProyecto