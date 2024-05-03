# encuestas\models.py
# imporamos los modelos de django
from django.db import models # importamos los modelos
from django.conf import settings # importamos las configuraciones de django

# La clase Encuesta define un modelo con campos para un nombre, descripción, 
# estado de disponibilidad, fecha de creación y una clave foránea 
# al modelo auth.Group.
# __str__(self): Este método devuelve el nombre de la instancia de 
# Encuesta cuando se convierte a una cadena, generalmente utilizado 
# para la representación del objeto.
class Encuesta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    disponible = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    grupo = models.ForeignKey('auth.Group', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

# Esta definición de clase es para un modelo llamado Pregunta.
# Campo encuesta: Es una clave externa al modelo Encuesta, con on_delete 
# configurado en CASCADE y related_name configurado en 'preguntas'.
# Campo texto: Es un campo TextField para almacenar el texto de la pregunta.
# Campo tipo: Es un CharField con una longitud máxima de 20 y opciones 
# establecidas en TIPO_PREGUNTA_CHOICES.
# Método __str__(self): Este método devuelve el atributo texto de la 
# instancia cuando se convierte a una cadena.
class Pregunta(models.Model): # Esta definición de clase es para un modelo llamado Pregunta.
    TIPO_PREGUNTA_CHOICES = [ # Campo tipo: Es un CharField con una longitud máxima de 20 y opciones establecidas en TIPO_PREGUNTA_CHOICES.
        ('texto_libre', 'Texto Libre'), # El campo texto es un CharField con una longitud máxima de 100.
        ('seleccion_unica', 'Selección Única'), # El campo texto es un CharField con una longitud máxima de 100.
        ('seleccion_multiple', 'Selección Múltiple'), # El campo texto es un CharField con una longitud máxima de 100.
    ]
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='preguntas')# La clave externa al modelo Encuesta, con on_delete configurado en CASCADE y related_name configurado en 'preguntas'.
    texto = models.TextField() # El campo texto es un CharField con una longitud máxima de 100.
    tipo = models.CharField(max_length=20, choices=TIPO_PREGUNTA_CHOICES) # El campo tipo es un CharField con una longitud máxima de 20 y opciones establecidas en TIPO_PREGUNTA_CHOICES.
    def __str__(self): # Este método devuelve el atributo texto de la instancia cuando se convierte a una cadena.
        return self.texto # Devuelve el atributo texto.
    
# La clase OpcionRespuesta define un modelo para una opción 
# de respuesta en una encuesta.
# __str__(self): Devuelve el atributo texto de la instancia 
# cuando se convierte a una cadena de texto.
class OpcionRespuesta(models.Model): # La clase OpcionRespuesta define un modelo para una opción de respuesta en una encuesta.
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones') # La clave externa al modelo Pregunta, con on_delete configurado en CASCADE y related_name configurado en 'opciones'.
    texto = models.CharField(max_length=100) # El campo texto es un CharField con una longitud máxima de 100.

    def __str__(self): # Este método devuelve el atributo texto de la instancia cuando se convierte a una cadena.
        return self.texto # Devuelve el atributo texto.
    
# La clase Prosepcto define un modelo para un prospecto.
# Clase Prospecto: Define un modelo para un prospecto.
# __str__(self): Devuelve el nombre del prospecto como una cadena.
class Prospecto(models.Model): # La clase Prosepcto define un modelo para un prospecto.
    nombre = models.CharField(max_length=100) # El campo nombre es un CharField con una longitud máxima de 100.
    correo = models.EmailField()    # El campo correo es un EmailField.
    telefono = models.CharField(max_length=15) # El campo telefono es un CharField con una longitud máxima de 15.
    # Añadir el campo para el asistente de admisión que registra al prospecto
    asistente = models.ForeignKey( # La clave externa al modelo settings.AUTH_USER_MODEL, con on_delete configurado en CASCADE y related_name configurado en 'prospectos'.
        settings.AUTH_USER_MODEL, # La clave externa al modelo settings.AUTH_USER_MODEL, con on_delete configurado en CASCADE y related_name configurado en 'prospectos'.
        on_delete=models.CASCADE, # Con este método, se elimina el usuario al que se hace referencia en la clave externa.
        related_name='prospectos', # El nombre de la clave externa relacionada.
    )
    def __str__(self): # Este método devuelve el nombre del prospecto como una cadena.
        return self.nombre # Devuelve el nombre del prospecto.
    
# la clase Respuesta define un modelo para una respuesta a una encuesta.
# prospecto: Establece una relación ForeignKey con el modelo Prospecto.
# usuario: Establece una relación ForeignKey con el modelo de Usuario.
# fecha: Almacena una fecha y hora de cuándo se creó la respuesta.
# pregunta: Establece una relación ForeignKey con el modelo Pregunta.
# encuesta: Establece una relación ForeignKey con el modelo Encuesta.
# texto_respuesta: Almacena una respuesta de texto con la opción de que esté en blanco.
# opciones_seleccionadas: Establece una relación ManyToManyField con el modelo OpcionRespuesta.
# __str__(self): Devuelve una representación de cadena del objeto Respuesta con el nombre del prospecto y el texto de la pregunta.
class Respuesta(models.Model): # la clase Respuesta define un modelo para una respuesta a una encuesta.
    prospecto = models.ForeignKey(Prospecto, on_delete=models.CASCADE, related_name='respuestas') # La clave externa al modelo Prospecto, con on_delete configurado en CASCADE y related_name configurado en 'respuestas'.
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='respuestas') # La clave externa al modelo settings.AUTH_USER_MODEL, con on_delete configurado en CASCADE y related_name configurado en 'respuestas'.
    fecha = models.DateTimeField(auto_now_add=True) # El campo fecha es un DateTimeField que se actualiza automáticamente cada vez que se crea una respuesta.
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas') # La clave externa al modelo Pregunta, con on_delete configurado en CASCADE y related_name configurado en 'respuestas'.
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='respuestas') # La clave externa al modelo Encuesta, con on_delete configurado en CASCADE y related_name configurado en 'respuestas'.
    texto_respuesta = models.TextField(blank=True, null=True) # El campo texto_respuesta es un TextField que puede estar vacío o no.
    opciones_seleccionadas = models.ManyToManyField(OpcionRespuesta, blank=True) #  La clave externa al modelo OpcionRespuesta, con on_delete configurado en CASCADE y related_name configurado en 'respuestas'.
    def __str__(self): # Este método devuelve una representación de cadena del objeto Respuesta con el nombre del prospecto y el texto de la pregunta.
        return f'Respuesta de {self.prospecto.nombre} a la pregunta: {self.pregunta.texto}' # Devuelve una representación de cadena del objeto Respuesta con el nombre del prospecto y el texto de la pregunta.
