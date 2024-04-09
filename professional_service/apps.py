from django.apps import AppConfig


class ProfessionalServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'professional_service'

    # register signals
    def ready(self):
        import professional_service.signals
