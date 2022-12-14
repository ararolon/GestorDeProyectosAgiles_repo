from dataclasses import field, fields
from enum import Flag
from pyexpat import model
from random import choices

from xml.etree.ElementInclude import include
from django import forms
from Proyectos.models import Proyecto
from UserStories.models import Estados_Kanban, TipoUSerStory, UserStories
from Proyectos.models import *

"""
Forms para la creacion de estados de kanban y tipos de user stories
"""

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
        self.fields['estados_kanban'].required = True
        self.fields['estados_kanban'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                       queryset= Estados_Kanban.objects.all().order_by('id'),initial=Estados_Kanban.objects.filter(defecto=True),
                                                                       label = "Seleccione los estados para el tablero Kanban")
        

    class Meta:
        model = TipoUSerStory
        fields = ['nombre','descripcion','estados_kanban']
   
    
    def clean(self):

        estados = self.cleaned_data['estados_kanban']
        contador = 0;
        for e in estados:
            if (e.nombre == 'Pendiente' or e.nombre == 'En curso' or e.nombre == 'Finalizado'):
                       contador = contador + 1 

        if contador != 3 :
            raise forms.ValidationError("No se pudo crear el Tipo de User Story , debe incluirse los estados obligatorios")               
    
           

class ModificarTipoUSForm(forms.ModelForm):
    """
    Formulario utilizado para modificar un tipo de US , se modifican el nombre y la descripcion.
    Formulario basado en el modelo TipoUserStory
    Clase Padre:
        form.ModelForm
    """
    def __init__(self,*args,**kwargs):
        """
        Constructor del Formulario.
        """
        super(ModificarTipoUSForm, self).__init__(*args, **kwargs)
        self.fields['estados_kanban'].empty_label = 'Seleccionar los estados para tablero Kanban'
        self.fields['estados_kanban'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                       queryset= Estados_Kanban.objects.all(),initial=Estados_Kanban.objects.filter(defecto=True),
                                                                       label = "Seleccione los estados para el tablero Kanban")

    
        
    class Meta:
        model = TipoUSerStory
        fields = ['nombre','descripcion','estados_kanban']

    def clean(self):

        estados = self.cleaned_data['estados_kanban']
        contador = 0;
        for e in estados:
            if (e.nombre == 'Pendiente' or e.nombre == 'En curso' or e.nombre == 'Finalizado'):
                       contador = contador + 1 

        if contador != 3 :
            raise forms.ValidationError("No se pudo modificar el Tipo de User Story , debe incluirse los estados obligatorios")               
    
           
        
class ImportarTipoUSForm(forms.ModelForm):
      """
      Form utilizado para importar tipos de user stories a un proyecto
      """
      def __init__(self,proyecto,*args,**kwargs):
       
            super(ImportarTipoUSForm, self).__init__(*args, **kwargs)
            self.fields['tipo_us'].label = "Tipos User stories del sistema"
            self.fields['tipo_us'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=TipoUSerStory.objects.all(),initial=proyecto.tipo_us.all())

      class Meta :
          model = Proyecto
          fields = ['tipo_us']
    




class UserStoryForm(forms.ModelForm):
   """
   Formulario utilizado para la creacion de un nuevo user story
   clase Padre:
         form.ModelForm        
   """
   def __init__(self,proyecto,*args,**kwargs):
        super(UserStoryForm, self).__init__(*args, **kwargs)

        self.fields['tipo']= forms.ModelChoiceField(queryset = proyecto.tipo_us.all())
        self.fields['PN'] = forms.IntegerField(min_value=1,max_value=10,label='Prioridad de Negocio (1-10)')
        self.fields['PT'] = forms.IntegerField(min_value=1, max_value=10, label='Prioridad Tecnica (1-10)')
        self.fields['horas_estimadas'].required = False
        self.fields['horas_estimadas'] = forms.IntegerField(min_value=0,max_value=100,initial=0)
        
   class Meta:
        model = UserStories
        fields = ['nombre','descripcion','tipo','PN','PT','comentarios','horas_estimadas']

        

class CambiarEstadoUSForm(forms.ModelForm):
    """
    Formulario utilizado para cambiar el estado de un user story
    clase Padre:
          form.ModelForm        
    """
    def __init__(self,proyecto,*args,**kwargs):
        """
        Constructor del Formulario.
        
        """
        super(CambiarEstadoUSForm, self).__init__(*args, **kwargs)
        self.fields['estado']= forms.ModelChoiceField(queryset = proyecto.tipo_us.all().first().estados_kanban.all())
        
    class Meta:
        model = UserStories
        fields = ['estado']

class ModificarUSForm(forms.ModelForm):

    """
    Formulario para modificar los datos de un US
    """

    disabled_fields = ('nombre,descripcion')

    def __init__(self,*args,**kwargs):
        
      super(ModificarUSForm, self).__init__(*args, **kwargs)
      self.fields['nombre'].disabled = True
      self.fields['descripcion'].disabled = True 


    class Meta:
        model = UserStories
        fields = ['nombre','descripcion','tipo','PN','PT','comentarios','horas_estimadas']