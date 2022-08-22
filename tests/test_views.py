
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse
from SSO.views import *

"""
test para las funciones de views.py del sistema
"""

class Test_views(TestCase):

    def setUp(self):
      self.client = Client()
      self.home_url = reverse('home')
      self.configuracion_inicial_url = reverse('configurar_sso')
      self.logout_url = reverse('logout')
      #creamos un usuario de prueba
      self.usuario = User.objects.create(username= 'test',first_name='ara', last_name='val', email='email@email.com')
      self.usuario.set_password('12345')
      self.usuario.save()
      self.user = User.objects.create(username='test2',first_name='jenn', last_name='cc', email='email2@email.com')
      self.user.set_password('1111')
      self.user.save()
      # crea el grupo de administrador
      group_name = "administrador"
      self.group = Group.objects.create(name=group_name)
      self.group.save()
      #crea el grupo de usuarios
      nombre_grupo="usuarios"
      self.grupo = Group.objects.create(name=nombre_grupo)
      self.grupo.save()
      self.usuario1=User.objects.create(username='test3',email='algunemail@mail.com')
      self.usuario1.set_password('456789')
      self.usuario1.save()

    def tearDown(self):
        self.user.delete()
        self.usuario.delete()
        self.group.delete()
        self.grupo.delete()

    def test_home_administrador(self):
        # agregamos al usuario al grupo de administrador
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='test2',password='1111')
        response = self.client.get(self.home_url)
        # verifica que el path sea /home
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response,'SSO/home.html')

    def test_redireccion_config_sso(self):
        #si no pertenece a ningun grupo,requiere configuracion
        self.client.login(username='test3',password='456789')
        response = self.client.get(self.home_url)
        self.assertTrue(response,self.configuracion_inicial_url)

    def test_home_usuarios(self):
        # se verifica que los usuarios usan su template
        self.user.groups.add(self.group)
        self.user.save()
        self.usuario.groups.add(self.grupo)
        self.usuario.save()
        self.client.login(username='test',password='12345')
        response = self.client.get(self.home_url)
        #verifica que el path sea /home
        self.assertTrue(response.status_code,200)
        self.assertTemplateUsed(response,'SSO/sinpermiso.html')

    def test_logout_view(self):
      response = self.client.get(self.logout_url)
      #pregunta si la vista redirecciona a la siguiente direccion
      self.assertTrue(response,redirect('/accounts/logout/'))

    def test_configuracion_inicial(self):
        response = self.client.get(self.configuracion_inicial_url)
        #redirecciona a home
        self.assertTrue(response,self.home_url)