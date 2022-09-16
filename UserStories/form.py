from django import forms

from UserStories.models import Estados_Kanban, TipoUSerStory

"""
 Archivo que define los formularios de creacion de tipos de US y
 estados de Kanban relacionado.
"""

class EstadosKanbanForm(forms.ModelForm):
  
  """
  Fomulario utilizado para crear un nuevo estado de un tablero Kanban 
  para un tipo de US
  Formulario basado en el modelo clase Estados_Kanban

  Clase Padre:
        form.ModelForm
  """

  def __init__(self,*args,**kwargs):
        """
        Constructor del Formulario.
        Agrega, en el campo 'permisos', los Permisos de Sistema que podrá tener el rol.
        """
        super(EstadosKanbanForm, self).__init__(*args, **kwargs)
 

  class Meta:
        model = Estados_Kanban
        fields = ['nombre']



class TiposUSForm(forms.ModelForm):
    """
    Formulario utilizado para crear un nuevo Tipo de User story en el sistema
    Formulario basado en el modelo TipoUserStory
    Clase Padre:
        form.ModelForm
    """
    def __init__(self,*args,**kwargs):
        """
        Constructor del Formulario.
        Agrega, en el campo 'permisos', los Permisos de Sistema que podrá tener el rol.
        """
        super(TiposUSForm, self).__init__(*args, **kwargs)
        self.fields['estados_kanban'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                                            choices=[(e.id, e.nombre) for e in Estados_Kanban.objects.all()
                                                                     ])

    class Meta:
        model = TipoUSerStory
        fields = ['nombre','prefijo','descripcion','estados_kanban']
