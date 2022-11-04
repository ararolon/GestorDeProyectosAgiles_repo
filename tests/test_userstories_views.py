from ast import arg
import pytest
from importlib.resources import path
from unicodedata import name
from urllib import response
from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, Client
from django.urls import reverse
from Proyectos.models import Proyecto
from UserStories.views import *

"""
Test para funciones de views.py UserStories
"""

@pytest.mark.django_db
class Test_userstories_views(TestCase):

    def setUp(self):
        tipo = TipoUSerStory.objects.create(nombre='prueba')
        self.client = Client()
        self.sprint = Sprint.objects.create(nombre_sprint='test',descripcion='prueba', estado_sprint = "En Curso", capacidad = 10)

        self.proyecto = Proyecto.objects.create(nombre='test',descripcion='prueba')
        self.proyecto.tipo_us.add(tipo)
        self.proyecto.sprint.add(self.sprint)
        self.proyecto.save()
        
        estado_inicial = Estados_Kanban.objects.create(nombre='inicial')
        self.estado = Estados_Kanban.objects.create(nombre='prueba')
        self.us = UserStories.objects.create(id_proyecto=self.proyecto.id,nombre='prueba', estado= estado_inicial)
        
        self.sprint.historias.add(self.us)
        self.sprint.id_proyecto = self.proyecto.id
        self.sprint.save()

    def test_crear_estadokanban(self):
        path = reverse('crear_estado',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code,200,"Error")
        self.assertTemplateUsed(response,'UserStories/crear_estado.html',"No se encontro el template indicado")

    
    def test_crear_tipo_us(self):

       path = reverse('crear_tipoUS',args=[self.proyecto.id])
       response = self.client.get(path)
       self.assertEqual(response.status_code,200,"Error")
       self.assertTemplateUsed(response,'UserStories/crear_tipoUS.html',"No se encontro el template indicado")


    def test_crear_us(self):

        path = reverse('crear_us',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code,200,"Error")
        self.assertTemplateUsed(response,'UserStories/crear_US.html',"No se encontro el template indicado")

    
    def test_importar_tipoUS(self):
        path = reverse('importar_tipoUS',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code,200,"Error")
        self.assertTemplateUsed(response,'UserStories/importar_tipoUS.html',"No se encontro el template indicado")


    def test_ver_product_backlog(self):
        path = reverse('product_backlog',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code,200,"Error")
        self.assertTemplateUsed(response,'UserStories/ver_product_backlog.html',"No se encontro el template indicado")

    def test_tablaKanban(self):
        path = reverse('tabla_kanban',args=[self.proyecto.id])
        response = self.client.get(path)
        self.assertEqual(response.status_code,200,"Error")
        self.assertTemplateUsed(response,'UserStories/tabla_kanban.html',"No se encontro el template indicado")

    def test_cambiarEstado(self):
        path = reverse('cambiarEstado', args=[self.us.id_us, self.estado.id]) 
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        # 302 found porque se redirige a la página de tabla_kanban
    
    def test_modificar(self):
        path = reverse('modificar_us', args=[self.proyecto.id,self.us.id_us]) 
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
