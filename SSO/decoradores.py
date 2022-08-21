
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User


def agregar_usuarios(view_func):
    """
    Decorador que se encarga de agregar al administrador y demas usuarios
    :param view_func: Una funcion vista
    :return: funcion decorador
    """
    def wrappper_func(request, *args, **kwargs):
        # si no hay todavia un administrador , toma el primer usuario que se registre en el sistema
        if User.objects.filter(groups__name = 'administrador').count() == 0:
            grupo = Group.objects.get(name='administrador')
            request.user.groups.add(grupo)

        # no esta en grupo administrador ni en grupo usuarios, entonces agregar a grupo usuario
        # siguientes usuarios que ingresan al sistema
        if not request.user.groups.filter(name='administrador').exists() and not request.user.groups.filter(
                name='usuarios').exists():
            # no es administrador , entonces se le agrega al grupo de usuarios
            # se verifica que no sea el superusuario de django
            if not request.user.is_superuser:
                grupo = Group.objects.get(name='usuarios')
                request.user.groups.add(grupo)

        return view_func(request, *args, **kwargs)
    return wrappper_func