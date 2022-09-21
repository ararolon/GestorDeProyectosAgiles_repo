import pytest
from http import HTTPStatus
from django.contrib.auth.models import User, Group, Permission
from permisos.models import RolesdeSistema
from Usuarios.models import Usuario
from django.test import TestCase, Client
from django.urls import reverse
#pruebas varias


@pytest.fixture
def rol():
    r = RolesdeSistema.objects.create(nombre='admin')
    r.save
    p= Permission.objects.get(content_type__app_label='permisos',codename='_crear_usuario')
    r.permisos.add(p)
    r.save()
    grupo = Group.objects.create(name=r.nombre)
    grupo.save()
    grupo.permissions.add(p)
    grupo.save()
    
    return grupo

@pytest.fixture
def usuario(rol):
   user = User.objects.create(username='test', password='pruebatest')
   user.save()
   user.groups.add(rol)
   return user


@pytest.fixture
def login(usuario):
    client = Client()
    client.login(username ='test',password='pruebatest')
    return client



@pytest.mark.django_db
class Testmodelusuario:
   
   """
   def test_listar_users(usuario,login):
    path= reverse('lista_users')
    response = login.get(path)
    assert response.status_code == HTTPStatus.OK
   """

   def desasignar_rol(usuario,rol):
    
      user = Usuario.objects.get(id=usuario.id)
      user.desasignar_rol(rol.id)    
      assert len(user.groups.all()) == 0

  
          
     




