from django import forms
from django.forms import inlineformset_factory
from .models import Encuesta, Pregunta, OpcionRespuesta, Prospecto, Respuesta
from django.contrib.auth.models import Group
# La clase PreguntaForm es un formulario basado en el modelo Pregunta.
# Meta: Contiene metadatos sobre el formulario, como el modelo, los campos 
# a incluir, etiquetas para los campos y widgets para personalizar los 
# tipos de entrada del formulario.
class PreguntaForm(forms.ModelForm): # La clase PreguntaForm es un formulario basado en el modelo Pregunta.
    class Meta: # Meta: Contiene metadatos sobre el formulario, como el modelo, los campos
        model = Pregunta # a incluir, etiquetas para los campos y widgets para personalizar los
        fields = ['texto', 'tipo'] # tipos de entrada del formulario.
        labels = {# Etiquetas para los campos
            'texto': '', # Texto de la pregunta
            'tipo': '', # Tipo de pregunta
        }
        widgets = { # Widgets para personalizar los tipos de entrada del formulario
            'texto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto de la pregunta', 'rows': 2}), # Texto de la pregunta
            'tipo': forms.Select(attrs={'class': 'form-control', 'rows': 2}), # Tipo de pregunta
        }
# Meta: Especifica metadatos para el formulario, incluyendo el modelo, campos, etiquetas y widgets.
# model: Especifica el modelo asociado con el formulario.
# fields: Especifica los campos del modelo para incluir en el formulario.
# labels: Especifica las etiquetas para los campos del formulario.
# widgets: Especifica los widgets para los campos del formulario.
class OpcionRespuestaForm(forms.ModelForm): # La clase OpcionRespuestaForm es un formulario basado en el modelo OpcionRespuesta.
    class Meta: # Meta: Especifica metadatos para el formulario, incluyendo el modelo, campos, etiquetas y widgets.
        model = OpcionRespuesta # model: Especifica el modelo asociado con el formulario.
        fields = ['texto'] # fields: Especifica los campos del modelo para incluir en el formulario.
        labels = { # labels: Especifica las etiquetas para los campos del formulario.
            'texto': 'Opción de respuesta', # Texto de la opción de respuesta
        } 
        widgets = { # widgets: Especifica los widgets para los campos del formulario.
            'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto de la opción de respuesta'}), # Texto de la opción de respuesta
        }
OpcionRespuestaFormSet = inlineformset_factory(Pregunta, OpcionRespuesta, form=OpcionRespuestaForm, extra=1, can_delete=True) # OpcionRespuestaFormSet es un conjunto de formularios basados en el modelo OpcionRespuesta.

# La clase EncuestaForm es un formulario que se utiliza para crear o actualizar una encuesta.
# nuevo_grupo_nombre: Define un campo para ingresar el nombre de un nuevo grupo.
# disponible: Define un campo para indicar si la encuesta está disponible.
# Meta: Proporciona metadatos para el formulario, como el modelo asociado (Encuesta), los campos 
# a mostrar (nombre, descripcion), y las etiquetas y widgets personalizados para cada campo.
class EncuestaForm(forms.ModelForm): # La clase EncuestaForm es un formulario que se utiliza para crear o actualizar una encuesta.
    nuevo_grupo_nombre = forms.CharField(label='Nombre del nuevo grupo', max_length=100, required=False) # nuevo_grupo_nombre: Define un campo para ingresar el nombre de un nuevo grupo.
    disponible = forms.BooleanField(label='Disponible', required=False) # disponible: Define un campo para indicar si la encuesta está disponible.

    class Meta: # Meta: Proporciona metadatos para el formulario, como el modelo asociado (Encuesta), los campos 
        model = Encuesta # a mostrar (nombre, descripcion), y las etiquetas y widgets personalizados para cada campo.
        fields = ['nombre', 'descripcion'] # campos a mostrar (nombre, descripcion)
        labels = { # labels: Especifica las etiquetas para los campos del formulario.
            'nombre': '', # Nombre de la encuesta
            'descripcion': '', # Descripción de la encuesta
        }
        widgets = { # widgets: Especifica los widgets para los campos del formulario.
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la encuesta'}), # Nombre de la encuesta
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la encuesta', 'rows': 2}), # Descripción de la encuesta
        }


# Esta definición de clase crea un formulario en Django para el modelo 
# Prospecto con campos para 'nombre', 'correo' y 'telefono'.
# model: Especifica el modelo al que está asociado el formulario.
# fields: Especifica los campos del modelo que se incluirán en el formulario.
# labels: Proporciona etiquetas para los campos del formulario.
# widgets: Especifica los widgets (tipos de entrada HTML) para cada campo del formulario.   
class ProspectoForm(forms.ModelForm): # La clase ProspectoForm es un formulario basado en el modelo Prospecto.
    class Meta: # Meta: Proporciona metadatos para el formulario, como el modelo, los campos, etiquetas y widgets.
        model = Prospecto # model: Especifica el modelo al que está asociado el formulario.
        fields = ['nombre', 'correo', 'telefono'] #     fields: Especifica los campos del modelo que se incluirán en el formulario.
        labels = { # labels: Proporciona etiquetas para los campos del formulario.
            'nombre': '', # Nombre del prospecto
            'correo': '', # Correo del prospecto
            'telefono': '', #       Telefono del prospecto
        }
        widgets = { # widgets: Especifica los widgets (tipos de entrada HTML) para cada campo del formulario.
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}), # Nombre del prospecto
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}), # Correo del prospecto
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}), #       Telefono del prospecto
        }

# El método model especifica el modelo asociado con el formulario.
# El método fields especifica los campos del modelo que se incluirán en el formulario.
# El método widgets especifica los widgets (tipos de entrada HTML) para cada campo del formulario.
class RespuestaForm(forms.ModelForm): # La clase RespuestaForm es un formulario basado en el modelo Respuesta.
    class Meta: # Meta: Proporciona metadatos para el formulario, como el modelo, los campos, etiquetas y widgets.
        model = Respuesta # model: Especifica el modelo al que está asociado el formulario.
        fields = ['prospecto', 'texto_respuesta', 'opciones_seleccionadas'] #     fields: Especifica los campos del modelo que se incluirán en el formulario.
        widgets = { # widgets: Especifica los widgets (tipos de entrada HTML) para cada campo del formulario.
            'prospecto': forms.HiddenInput(),  # Campo oculto para el Prospecto
            'texto_respuesta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tu respuesta aquí'}), # Texto de la respuesta
            'opciones_seleccionadas': forms.CheckboxSelectMultiple(), # Opciones de respuesta
        }

