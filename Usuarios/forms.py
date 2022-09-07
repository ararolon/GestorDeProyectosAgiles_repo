from django import forms

from permisos.models import RolesdeSistema


class AsignarRolForm(forms.Form):
    """
    Formulario utilizado para asignar  un rol de Sistema a un Usuario.
    Clase Padre:
        form.ModelForm
    """

    def __init__(self, *args, usuario=None, **kwargs):
        """
        Constructor del Formulario.
        Agrega, en el campo 'Rol', los Roles que el Usuario podrá tener.
        """
        super(AsignarRolForm, self).__init__(*args, **kwargs)
        self.usuario = usuario
        self.fields['Roles'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,choices=[(p.id, p.nombre) for p in RolesdeSistema.objects.all()])
     
