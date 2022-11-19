from django.contrib import admin
from .models import Estados_Kanban,TipoUSerStory,UserStories, HoraPorDia

# Register your models here.

admin.site.register(TipoUSerStory)
admin.site.register(Estados_Kanban)
admin.site.register(UserStories)
admin.site.register(HoraPorDia)