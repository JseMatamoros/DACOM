from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
# Este fragmento de código es un receptor de señal en Django que se 
# activa después de que se guarda una instancia de Usuario. 
# Verifica si el usuario es recién creado, recupera el nombre del 
# grupo seleccionado de la instancia de usuario y agrega el usuario 
# al grupo correspondiente si existe.
@receiver(post_save, sender=User)
def assign_user_to_selected_group(sender, instance, created, **kwargs):
    if created:  # si el usuario es recién creado
        selected_group = instance.selected_group # suponiendo que el nombre del grupo seleccionado se almacena en selected_group_name
        try: # verificar si el grupo ya existe o crearlo si no existe
            group = Group.objects.get(name=selected_group) # obtener el grupo
            instance.groups.add(group) # agregar el usuario al grupo
        except Group.DoesNotExist: # si el grupo no existe
            pass # no hacer nada
