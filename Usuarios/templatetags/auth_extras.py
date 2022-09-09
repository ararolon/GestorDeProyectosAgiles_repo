from atexit import register
from django import template
from django.contrib.auth.models import Group

"""
    Archivo que permite realizar consultas sobre si un usuario pertenece a un grupo o no dentro de un template
"""

register = template.Library()

@register.filter(name='has_group')
def has_group(user,group_name):
     group = Group.objects.get(name=group_name)
     return True if group in user.groups.all() else False 