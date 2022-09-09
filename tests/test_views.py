
from http import client
from urllib import response
import pytest
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse
from SSO.views import *
from permisos.models import RolesdeSistema

"""
test para las funciones de views.py del sistema
"""
@pytest.mark.django_db
class Test_views(TestCase):
    """
        tests para views de app SSO
    """
    def setUp(self):
      """
       Se defienen las variables de prueba
      """
      
      self.client = Client()
      self.home_url = reverse('home')
      self.login_url = reverse('login')
      self.configuracion_inicial_url = reverse('configurar_sso')
      self.logout_url = reverse('logout')
      #creamos un usuario de prueba
      self.usuario = User.objects.create(username= 'test',first_name='ara', last_name='val', email='email@email.com')
      self.usuario.set_password('12345')
      self.usuario.save()
      self.user = User.objects.create(username='test2',first_name='jenn', last_name='cc', email='email2@email.com')
      self.user.set_password('1111')
      self.user.save()
      self.usuario1=User.objects.create(username='test3',email='algunemail@mail.com')
      self.usuario1.set_password('456789')
      self.usuario1.save()
      self.user3 = User.objects.create(username='test4',email='email@mail.com')
      self.user3.set_password('123456')
      self.rol_admin = RolesdeSistema.objects.create(nombre="administrador")
      self.rol_admin.save()
      self.rol_usuarios = RolesdeSistema.objects.create(nombre="usuarios")
      self.rol_usuarios.save()
      self.rol_sin_acceso = RolesdeSistema.objects.create(nombre="sin_acceso")
      self.rol_sin_acceso.save()
      self.grupo_admin = Group.objects.create(name=self.rol_admin.nombre)
      self.grupo_usuarios = Group.objects.create(name=self.rol_usuarios.nombre)
      self.grupo_sin_acceso = Group.objects.create(name=self.rol_sin_acceso.nombre)


    def tearDown(self):
        self.user.delete()
        self.usuario.delete()
        self.usuario1.delete()
        self.user3.delete()
        self.grupo_admin.delete()
        self.rol_admin.delete()
        self.rol_sin_acceso.delete()
        self.rol_usuarios.delete()
        self.grupo_usuarios.delete()
        self.grupo_sin_acceso.delete()

    def test_home_administrador(self):
        """
        Prueba si cuando el usuario que se logea es el administrador del sistema , redirecciona al template de home de administrador
        """
        # agregamos al usuario al grupo de administrador
        self.user.groups.add(Group.objects.get(name=self.rol_admin.nombre))
        self.user.save()
        self.client.login(username='test2',password='1111')
        response = self.client.get(self.home_url)
        # verifica que el path sea /home
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response,'SSO/home_admin.html',"No se encuentra este template")

    
    def test_redireccion_config_sso(self):
        #si no pertenece a ningun grupo,requiere configuracion
        self.client.login(username='test3',password='456789')
        response = self.client.get(self.home_url)
        self.assertTrue(response,self.configuracion_inicial_url)
    
    
    def test_no_logueado(self):
        """
        Prueba que un usuario que no se encuentra logueado , sea restringido al insicio del sistema
        """
        
        response = self.client.get(self.login_url)
        self.assertTrue(response.status_code,200)


    def test_logout_view(self):
      response = self.client.get(self.logout_url)
      #pregunta si la vista redirecciona a la siguiente direccion
      self.assertTrue(response,redirect('/accounts/logout/'))

  
