from re import T
from django import forms
from django.contrib.auth.models import Group

from Proyectos.models import Proyecto
import datetime
from functools import partial
from django.forms import fields
from Usuarios.models import *
from Proyectos.models import RolUsuario

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class crearproyectoForm(forms.ModelForm):
    """
    Form que permite la creacion de un nuevo proyecto.
    Es necesario especificar el scrumMaster del proyecto.
        -nombre: str, nombre del proyecto
        -descripcion: str, descripcion del proyecto
        -scrumMaster: Usuario que se le asignar el rol de scrumMaster del proyecto
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
    
    
class AsignarMiembroForm(forms.ModelForm):
    """
    Form que permite asignar miembros al proyecto
    """
    disabled_fields = ('nombre', 'descripcion', 'scrumMaster')

    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion', 'miembros', 'scrumMaster')
        
    def __init__(self, *args, **kwargs):
        super(AsignarMiembroForm, self).__init__(*args, **kwargs)
        self.fields['miembros'].widget = forms.CheckboxSelectMultiple()
        self.fields['miembros'].queryset = Usuario.objects.exclude(id=self.instance.scrumMaster.id).filter(groups__name='usuarios')

        for field in self.disabled_fields:
            self.fields[field].disabled = True

class ImportarRolForm(forms.ModelForm):
    """
    Form que permite importar roles de un proyecto a otro
    """

    class Meta:
        model = Proyecto
        fields = ('roles',)
        
    def __init__(self, *args, **kwargs):
        super(ImportarRolForm, self).__init__(*args, **kwargs)
        self.fields['roles'].widget = forms.CheckboxSelectMultiple()
        self.fields['roles'].queryset = RolesdeSistema.objects.filter(defecto=False)

class AsignarRolForm(forms.ModelForm):
    """
    Form que permite asignar roles a un miembro del proyecto
    """
    disabled_fields = ()
    # disabled_fields = ('miembro',)

    class Meta:
        model = RolUsuario
        fields = ('roles',)
        
    def __init__(self, id_proyecto, *args, **kwargs):
        super(AsignarRolForm, self).__init__(*args, **kwargs)
        self.fields['roles'].widget = forms.CheckboxSelectMultiple()
        self.fields['roles'].queryset = RolesdeSistema.objects.filter(proyecto=id_proyecto)

        for field in self.disabled_fields:
            self.fields[field].disabled = True