from django.apps import AppConfig
# Esta definición de clase es para configurar la aplicación 'accounts' en Django.
# default_auto_field: Especifica el tipo de campo de clave primaria predeterminado.
# name: Especifica el nombre de la aplicación.
# ready: Importa las señales cuando la aplicación está lista.
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Importar las señales de la aplicación