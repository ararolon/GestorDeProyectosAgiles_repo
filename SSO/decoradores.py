
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User
from Usuarios.models import Usuario


def agregar_usuarios(view_func):
    """
    Decorador que se encarga de agregar al administrador y demas usuarios
    :param view_func: Una funcion vista
    :return: funcion decorador
    """
    def wrappper_func(request, *args, **kwargs):
        # si no hay todavia un administrador , toma el primer usuario que se registre en el sistema
        if User.objects.filter(groups__name = 'administrador').count() == 0:
            admin = Usuario.objects.get(id = request.user.id)
            admin.dar_permisos_administrador()

        # no esta en grupo administrador ni en grupo usuarios, entonces agregar a grupo usuario
        # siguientes usuarios que ingresan al sistema
        if not request.user.groups.filter(name='administrador').exists() and not request.user.groups.filter(
                name='usuarios').exists():
            # no es administrador y no pertenece al grupo de usuarios, entonces se le agrega al grupo sin_acceso , usuarios que no tienen acceso al sistema
            # se verifica que no sea el superusuario de django
            if not request.user.is_superuser:
                grupo = Group.objects.get(name='sin_acceso')
                request.user.groups.add(grupo)

        return view_func(request, *args, **kwargs)
    return wrappper_func