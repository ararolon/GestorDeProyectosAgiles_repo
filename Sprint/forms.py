from django import forms
from .models import Sprint,estadoSprint
from functools import partial
from Usuarios.models import *
from Proyectos.models import *

from Sprint.sprint import sprintProyecto
from UserStories.models import Estados_Kanban, TipoUSerStory, UserStories

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class crearSprintForm(forms.ModelForm):
    """
    Form que permite la creacion de un nuevo Sprint.
    """
    nombre_sprint = forms.CharField(label="Nombre del Sprint", widget=forms.Textarea(attrs={"rows": 1, "cols": 20}))
    duracion_sprint = forms.IntegerField(label="Duración de los Sprints en días", min_value=7,max_value=30)
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    class Meta:
        model = Sprint
        fields = ('nombre_sprint', 'duracion_sprint', 'descripcion','id_proyecto')

    def __init__(self, id_proyecto,*args, **kwargs):
        super(crearSprintForm, self).__init__(*args, **kwargs)
        self.fields['id_proyecto'] = forms.IntegerField(widget=forms.HiddenInput(), initial=id_proyecto)

    def clean(self):
        borrar_datos = super().clean()
        # if(sprintProyecto.sprint_creado(self)):
        print(borrar_datos)
        if(Sprint.objects.filter(id_proyecto=borrar_datos["id_proyecto"]).filter(estado_sprint=estadoSprint.EN_PLANIFICACION).exists()):
            raise forms.ValidationError('No se pudo crear. Ya existe un sprint en planificación')
        return borrar_datos


class MiembroSprintForm(forms.ModelForm):
    """
    Form que permite asignar miembros del Proyecto a un Sprint
    """
    disabled_fields = ('nombre_sprint', 'descripcion')

    class Meta:
        model = Sprint
        fields = ('nombre_sprint', 'descripcion', 'miembros_sprint','capacidad')
        
    def __init__(self, *args, **kwargs):
        super(MiembroSprintForm, self).__init__(*args, **kwargs)
        self.fields['miembros_sprint'].widget = forms.CheckboxSelectMultiple()
        # self.fields['miembros_sprint'].queryset = Usuario.objects.exclude(id=self.instance.scrumMaster.id).filter(groups__name='usuarios')
        self.fields['miembros_sprint'].queryset = Usuario.objects.all()

        for field in self.disabled_fields:
            self.fields[field].disabled = True


class AsignarUSSprintForm(forms.ModelForm):
    """
    Formulario para asignar user stories en un sprint.
    Se considera que un US debe tener asignado horas de esfuerzo para poder ser asignado a un Sprint.
    """
    
    def __init__(self,proyecto,sprint,*args, **kwargs):
        super(AsignarUSSprintForm,self).__init__(*args, **kwargs)
        #Obtiene los US que tengan horas estimadas asignadas , es decir horas estimadas >0 y ordena por prioridad , de mayor a menor
        self.fields['historias'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                          queryset= UserStories.objects.filter(id_proyecto = proyecto.id).filter(horas_estimadas__gte = 1).order_by('-Prioridad').exclude(estado= Estados_Kanban.objects.get(nombre='Finalizado')).exclude(estado = Estados_Kanban.objects.get(nombre='Cancelado')),
                                                           label= 'Seleccione los User Stories que seran trabajados en el Sprint',initial=sprint.historias.all())


    class Meta:
            model = Sprint
            fields = ['historias']

     
