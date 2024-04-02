from django.apps import AppConfig


class DoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'professional'

    # register signals
    def ready(self):
        import professional.signals
