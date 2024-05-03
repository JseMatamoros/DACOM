from django.contrib import admin
from .models import Encuesta, Pregunta, OpcionRespuesta, Prospecto, Respuesta

@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'disponible','fecha_creacion', 'grupo']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['fecha_creacion']

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'tipo', 'encuesta']
    search_fields = ['texto']
    list_filter = ['encuesta']

@admin.register(OpcionRespuesta)
class OpcionRespuestaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'pregunta']
    search_fields = ['texto']
    list_filter = ['pregunta']

@admin.register(Prospecto)
class ProspectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'correo', 'telefono']
    search_fields = ['nombre', 'correo', 'telefono']

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ['prospecto', 'pregunta', 'texto_respuesta']
    search_fields = ['prospecto__nombre', 'pregunta__texto']
