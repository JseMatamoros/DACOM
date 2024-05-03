from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Esta definición de clase personaliza la interfaz admin para el modelo CustomUser. 
# list_display: Define qué campos se muestran en la lista de usuarios en el panel de administración.
# search_fields: Especifica los campos que se pueden usar para buscar usuarios en el panel de administración.
# list_filter: Especifica los campos que se pueden usar para filtrar usuarios en el panel de administración.
# fieldsets: Agrupa los campos mostrados al editar un usuario en el panel de administración.
# filter_horizontal: Especifica los campos mostrados en una lista de filtro horizontal.
class CustomUserAdmin(UserAdmin):
    # campos que se mostrarán en la lista de usuarios en el panel de administración
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    # campos que se pueden utilizar para buscar usuarios en el panel de administración
    search_fields = ['username', 'email', 'first_name', 'last_name']
    # campos que se pueden filtrar en el panel de administración
    list_filter = ['is_staff', 'is_active']
    # campos que se mostrarán al editar un usuario en el panel de administración
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
        ('Información adicional', {'fields': ('selected_group',)}),  # Agregar el campo selected_group
    )
    # campos que se mostrarán en la lista de filtrado horizontal
    filter_horizontal = ['groups', 'user_permissions']
# registra tu modelo CustomUser con el CustomUserAdmin personalizado
admin.site.register(CustomUser, CustomUserAdmin)
