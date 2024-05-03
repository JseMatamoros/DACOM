from django.apps import AppConfig

class EncuestasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'encuestas'

    def ready(self):
        # Import signals here
        import encuestas.signals
