from django import forms
from Sprint.models import Sprint, SprintMiembros,estadoSprint
from functools import partial
from UserStories.models import Estados_Kanban
from Usuarios.models import *
from Proyectos.models import *
from Sprint.sprint import sprintProyecto
from UserStories.models import Estados_Kanban

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class crearSprintForm(forms.ModelForm):
    """
    Formulario que permite la creacion de un nuevo Sprint
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


class modificarSprintForm(forms.ModelForm):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos que son necesarios 
    para la modificación de un sprint, el formulario permite modificar los campos: 'nombre sprint',
    'descripcion' y 'fecha fin'
    """
    disabled_fields = ('duracion_sprint','fecha_creacion', 'fecha_inicio')

    nombre_sprint = forms.CharField(label="Nombre del Sprint", widget=forms.Textarea(attrs={"rows": 1, "cols": 20}))
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))
   
    def __init__(self,*args, **kwargs):
        super(modificarSprintForm, self).__init__(*args, **kwargs)
        
        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Sprint
        fields = ('nombre_sprint', 'duracion_sprint', 'fecha_creacion', 'fecha_inicio', 'descripcion')


class MiembroSprintForm(forms.ModelForm):
    """
    Formulario que permite asignar miembros del Proyecto a un Sprint
    """
    class Meta:
        model = SprintMiembros
        fields = ('miembro','capacidad_miembro','sprint',)

    capacidad_miembro = forms.IntegerField(label="Capacidad del usuario en horas", min_value=0)

    def __init__(self,id_sprint,*args, **kwargs):
        super(MiembroSprintForm, self).__init__(*args, **kwargs)
        self.fields['sprint'].initial = id_sprint
        sprint = Sprint.objects.get(id=id_sprint)
        self.fields['miembro'].empty_label = 'Seleccionar Miembro'
        self.fields['miembro'].queryset = Proyecto.objects.get(id=sprint.id_proyecto).miembros
        
    def clean(self):
        datos = super().clean()
        if(SprintMiembros.objects.filter(sprint=datos['sprint']).filter(miembro=datos["miembro"]).exists()):
            raise forms.ValidationError('El miembro ya ha sido asignado')
        return datos    
