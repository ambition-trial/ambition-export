from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'ambition_export'
    verbose_name = 'Ambition Export'
