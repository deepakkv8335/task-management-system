from django.apps import AppConfig

class TmsappConfig(AppConfig):
    name = 'tmsapp'

    def ready(self):
        import tmsapp.signals
