from django import forms
from django.contrib.auth.models import Permission

from .models import RolesdeSistema


class NewRolForm(forms.ModelForm):
    """
    Formulario utilizado para crear un nuevo Rol de Sistema
    Este formulario esta basado en el Modelo RolDeSistema.
    Clase Padre:
        form.ModelForm
    """
    def __init__(self,*args,**kwargs):
        """
        Constructor del Formulario.
        Agrega, en el campo 'permisos', los Permisos de Sistema que podrá tener el rol.
        """
        super(NewRolForm, self).__init__(*args, **kwargs)
        self.fields['permisos'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                                            choices=[(p.id, p.name) for p in Permission.objects.all()
                                                                     if p.codename.startswith('_')])

    class Meta:
        model = RolesdeSistema
        fields = ['nombre','descripcion','permisos']