from django import forms
from django.contrib.auth.models import Group

from Proyectos.models import Proyecto
import datetime
from functools import partial
from django.forms import fields
from Usuarios.models import *

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class crearproyectoForm(forms.Form):
    """
    Form que permite la creacion de un nuevo proyecto.
    Es necesario especificar el scrumMaster del proyecto.
    Campos:
        -nombre: str, nombre del proyecto
        -descripcion: str, descripcion del proyecto
        -scrumMaster: User, usuario que se le asignar el rol de scrumMaster del proyecto
    """

    nombre = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 20}))

    descripcion = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    scrumMaster = forms.ModelChoiceField(queryset=Usuario.objects.filter(groups__isnull=False), empty_label='Seleccionar Scrum Master para el proyecto')


    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion', 'scrumMaster')



    def __init__(self, *args, **kwargs):
    
       super(crearproyectoForm, self).__init__(*args, **kwargs)
       self.fields['scrumMaster'].empty_label = 'Seleccionar Scrum Master para el proyecto'
       self.fields['scrumMaster'].queryset = Usuario.objects.filter(groups__isnull=False)
    
    