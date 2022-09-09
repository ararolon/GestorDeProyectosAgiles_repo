from ast import arg
from importlib.resources import path
from urllib import response
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse
from permisos.views import *
from permisos.models import RolesdeSistema


"""
    Test para funciones de views.py de Usuarios
"""

class Test_usuarios_views(TestCase):

  def setUp(self):
    self.client = Client()
    self.usuario = User.objects.create(username='test')



  def test_lista_eliminar(self):

    path = reverse('index_eliminar')
    response = self.client.get(path)
    self.assertEqual(response.status_code,200)
    self.assertTemplateUsed(response,'Usuarios/index_eliminar.html')
    
  def test_eliminar_usuario(self):
       path = reverse('eliminar_user', args=[self.usuario.id])
       response = self.client.get(path)
       self.assertTemplateUsed(response,'Usuarios/eliminar.html')

  def test_listar_usuarios(self):
      path = reverse('lista_users')
      response = self.client.get(path)
      self.assertEqual(response.status_code,200)
      self.assertTemplateUsed(response,'Usuarios/listar_usuarios.html')

  def test_crear_usuario(self): 
      path = reverse('dar_acceso', args=[self.usuario.id])
      response = self.client.get(path)
      self.assertTemplateUsed(response,'Usuarios/Daracceso.html')

  def test_asignar_rol_usuario(self):
      path = reverse('asignar_rol', args=[self.usuario.id])
      response = self.client.get(path)
      self.assertTemplateUsed(response,'Usuarios/asignar_rol.html')


