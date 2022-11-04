
import pytest
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from SSO.views import home, login, logout, configurar_sso

"""
test para los urls del sistema
"""
class Test_urls(SimpleTestCase):

  def test_home(self):
    url = reverse('home')
    self.assertEqual(resolve(url).func, home, "no se pudo dirigir a el url home")


  def test_login(self):
    url = reverse('login')
    self.assertEqual(resolve(url).func,login)

  def test_logout(self):
    url = reverse('logout')
    self.assertEqual(resolve(url).func,logout)
  
  def test_configurar_sso(self):
    url = reverse('configurar_sso')
    self.assertEqual(resolve(url).func,configurar_sso)

       
