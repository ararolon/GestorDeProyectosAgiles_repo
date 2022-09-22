from django import forms
from Sprint.models import Sprint
from functools import partial
from Usuarios.models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class crearSprintForm(forms.ModelForm):
    """
    Form que permite la creacion de un nuevo proyecto.
    Es necesario especificar el scrumMaster del proyecto.
        -nombre: str, nombre del proyecto
        -descripcion: str, descripcion del proyecto
        -scrumMaster: Usuario que se le asignar el rol de scrumMaster del proyecto
    """
    nombre_sprint = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 20}))
    duracion_sprint = forms.IntegerField(label="Duración de los sprints (en días)", min_value=0)
    fecha_inicio = forms.DateField(label="Fecha de inicio",
                                   widget=forms.DateInput(attrs={'onchange': 'actualizar_fecha_fin()'}),
                                   error_messages={'invalid': 'La fecha debe estar en formato dd/mm/aaaa.'})
    fecha_fin = forms.DateField(label="Fecha de fin",
                                   widget=forms.DateInput(attrs={'onchange': 'actualizar_fecha_fin()'}),
                                   error_messages={'invalid': 'La fecha debe estar en formato dd/mm/aaaa.'})
    descripcion = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    class Meta:
        model = Sprint
        fields = ('nombre_sprint', 'duracion_sprint', 'fecha_inicio', 'fecha_fin', 'descripcion')

    def __init__(self, *args, **kwargs):
       super(crearSprintForm, self).__init__(*args, **kwargs)

   


