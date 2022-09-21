from dataclasses import field
from xml.etree.ElementInclude import include
from django import forms

"""
Forms para la creacion de estados de kanban y tipos de user stories
"""


from UserStories.models import Estados_Kanban, TipoUSerStory, UserStories

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
        """
        super(TiposUSForm, self).__init__(*args, **kwargs)
        self.fields['estados_kanban'].empty_label = 'Seleccionar los estados para tablero Kanban'
        self.fields['estados_kanban'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                                            choices=[(e.id, e.nombre) for e in Estados_Kanban.objects.all()
                                                                     ])

    class Meta:
        model = TipoUSerStory
        fields = ['nombre','descripcion','estados_kanban']


class UserStoryForm(forms.ModelForm):
   """
   Formulario utilizado para la creacion de un nuevo user story
   clase Padre:
         form.ModelForm        
   """
   def __init__(self,*args,**kwargs):
        """
        Constructor del Formulario.
        
        """
        PRIORIDAD_CHOICES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
        ]
   
        super(UserStoryForm, self).__init__(*args, **kwargs)
        self.fields['prioridad'].empty_label = 'Seleccionar la prioridad del User Story'
        self.fields['prioridad']= forms.ChoiceField(widget=forms.RadioSelect, choices=PRIORIDAD_CHOICES)
    
   class Meta:
        model = UserStories
        fields = ['nombre','descripcion','tipo','prioridad','comentarios','horas_estimadas']



