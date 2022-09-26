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

class Test_userstories_views(TestCase):

    def setUp(self):
        self.client = Client()
        self.proyecto = Proyecto.objects.create(nombre='test',descripcion='prueba')
        self.proyecto.save()


    def   test_crear_estadokanban(self):
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