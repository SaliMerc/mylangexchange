from django.apps import AppConfig


class LangAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lang_app'

    def ready(self):
        import lang_app.signals
