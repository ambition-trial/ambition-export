from django.apps import AppConfig as DjangoAppConfig
from django.core.checks.registry import register

from .system_checks import export_folder_check


class AppConfig(DjangoAppConfig):
    name = 'ambition_export'
    verbose_name = 'Ambition Export'

    def ready(self):
        register(export_folder_check)
