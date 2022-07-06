from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'my_app'
    def ready(self):
        import my_app.signals

