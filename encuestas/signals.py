from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import Encuesta

# Este fragmento de código define una señal que se activa después de 
# eliminar un objeto de la clase Encuesta. Cuando se elimina un objeto, 
# si tiene un grupo asociado, se elimina también ese grupo.
@receiver(post_delete, sender=Encuesta) # activar cuando se elimina una encuesta
def eliminar_grupo_encuesta(sender, instance, **kwargs): # sender y instance como parámetros
    if instance.grupo: # si la encuesta tiene un grupo
        instance.grupo.delete() # elimina el grupo

# Este código Python se ejecuta después de guardar una instancia de la 
# clase Encuesta. En resumen, asigna permisos específicos a un grupo de 
# usuarios basados en el nombre del grupo proporcionado en el formulario 
# de creación de la encuesta. Los permisos se obtienen de ciertas acciones 
# relacionadas con encuestas, respuestas, prospectos, preguntas y opciones 
# de respuesta. Una vez obtenidos, se asignan al grupo de usuarios. 
@receiver(post_save, sender=Encuesta) # activar cuando se crea una encuesta
def asignar_permisos_a_grupo(sender, instance, created, **kwargs): # sender, instance y created como parámetros
    if created: # si la encuesta es recien creada
        # obtener el nombre del grupo desde el formulario de creación de la encuesta
        nombre_grupo = instance.grupo  # reemplaza esto con el campo correcto
        # Verificar si el grupo ya existe o crearlo si no existe
        grupo, created = Group.objects.get_or_create(name=nombre_grupo)
        # Obtener los permisos necesarios
        permisos = Permission.objects.filter(
            content_type__app_label='encuestas',
            codename__in=['view_encuesta', 'add_respuesta', 'add_prospecto', 'view_pregunta', 'view_opcionrespuesta']
        )
        # print statement para verificar los permisos obtenidos
        print("Permisos obtenidos:", permisos)
        # asignar los permisos al grupo
        grupo.permissions.add(*permisos)