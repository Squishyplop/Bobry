from django.apps import AppConfig


class BobryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bobry'

    def ready(self):
        import bobry.signals