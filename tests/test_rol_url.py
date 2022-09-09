import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from permisos.views import modificar_rol, listar_roles, crear_rol, eliminar_rol
from permisos.models import RolesdeSistema

"""
test para los urls de los roles del sistema
"""
class Test_urls(TestCase):

  def setUp(self):
    self.rol = RolesdeSistema.objects.create(nombre='testRol', descripcion='testRol')


  def test_crearRol(self):
    url = reverse('crear_rol')
    self.assertEqual(resolve(url).func, crear_rol, "no se pudo dirigir a el url home")

  def test_eliminarRol(self):
    url = reverse('eliminar_rol', args=[self.rol.id])
    self.assertEqual(resolve(url).func, eliminar_rol)

  def test_listarRoles(self):
    url = reverse('listar_roles')
    self.assertEqual(resolve(url).func, listar_roles)
  
  def test_modificarRol(self):
    url = reverse('modificar_rol', args=[self.rol.id])
    self.assertEqual(resolve(url).func, modificar_rol)
   

