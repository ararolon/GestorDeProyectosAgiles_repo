from django.contrib import admin

from .models import Proyecto,RolUsuario, historia

admin.site.register(Proyecto)
admin.site.register(RolUsuario)
admin.site.register(historia)