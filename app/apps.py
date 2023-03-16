from django.apps import AppConfig
from . import job

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from . import job
        job.start()
      