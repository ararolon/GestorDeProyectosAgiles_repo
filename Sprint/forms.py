from django import forms
from Sprint.models import Sprint,estadoSprint
from functools import partial
from Usuarios.models import *
from Proyectos.models import *
from Sprint.sprint import sprintProyecto

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class crearSprintForm(forms.ModelForm):
    """
    Form que permite la creacion de un nuevo Sprint.
    """
    nombre_sprint = forms.CharField(label="Nombre del Sprint", widget=forms.Textarea(attrs={"rows": 1, "cols": 20}))
    duracion_sprint = forms.IntegerField(label="Duración de los Sprints en días", min_value=0)
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
        
        
