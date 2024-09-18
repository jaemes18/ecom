from django.apps import AppConfig


class BooktConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecom'
    def ready(self):
        import ecom.signals

