from django import forms
from Sprint.models import Sprint
from functools import partial
from Usuarios.models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class crearSprintForm(forms.ModelForm):
    """
    Form que permite la creacion de un nuevo Sprint.
    """
    nombre_sprint = forms.CharField(label="Nombre del Sprint", widget=forms.Textarea(attrs={"rows": 1, "cols": 20}))
    duracion_sprint = forms.IntegerField(label="Duración de los Sprints (en días)", min_value=0)
    fecha_inicio = forms.DateField(label="Fecha de inicio",
                                   widget=forms.DateInput(attrs={'onchange': 'actualizar_fecha_inicio()'}),
                                   error_messages={'invalid': 'La fecha debe estar en formato dd/mm/aaaa.'})
    fecha_fin = forms.DateField(label="Fecha de finalización",
                                   widget=forms.DateInput(attrs={'onchange': 'actualizar_fecha_fin()'}),
                                   error_messages={'invalid': 'La fecha debe estar en formato dd/mm/aaaa.'})
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    class Meta:
        model = Sprint
        fields = ('nombre_sprint', 'duracion_sprint', 'fecha_inicio', 'fecha_fin', 'descripcion')

    def __init__(self, *args, **kwargs):
       super(crearSprintForm, self).__init__(*args, **kwargs)

   
