from unittest import TestCase
import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from Usuarios.views import *
from django.contrib.auth.models import User, Group, Permission


"""
Archivo para pruebas de urls de la app Usuarios
"""

class Test_urls(TestCase):

    def setUp(self):
        self.user =  User.objects.create(username='test')



    def test_eliminar_rol(self): 
        """
        prueba de si el url asocia con la view 
        """
        url = reverse('eliminar_user', args=[self.user.id])
        self.assertEqual(resolve(url).func,eliminar_usuario)  

    def test_index_usuario(self):
        """
        prueba el url de index eliminar usuarios
        """
        url = reverse('index_eliminar')
        self.assertEqual(resolve(url).func,lista_eliminar)


    def test_listar_usuarios(self):
        """
        prueba el url de listar usuarios
        """
        url = reverse('lista_users')
        self.assertEqual(resolve(url).func,listar_usuarios)

    def test_dar_acceso(self):
       """
       Prueba el url de dar acceso
       """
       
       url = reverse('dar_acceso', args=[self.user.id])
       self.assertEqual(resolve(url).func,crear_usuario)

    def test_asignar_rol(self):
        """
        Prueba de url de asignar roles a un usuario
        """
        url = reverse('asignar_rol', args=[self.user.id])
        self.assertEqual(resolve(url).func,asignar_rol_usuario)

    def test_ver_notificaciones(self):
        url = reverse('notificaciones',args=['user.username'])
        self.assertEqual(resolve(url).func,ver_notificaciones)

    def test_listar_notificaciones(self):
        url = reverse('lista_notis',args=['user.username'])
        self.assertEqual(resolve(url).func,listar_notificaciones)

    def test_listar_notificaciones_usuarios(self):
        url = reverse('listar_notis_user',args=['user.username'])
        self.assertEqual(resolve(url).func,listar_notificaciones)

   
   

         