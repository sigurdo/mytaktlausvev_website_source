from django.apps import AppConfig

# Checks must be imported into a file loaded by Django
from . import checks  # noqa


class CommonConfig(AppConfig):
    name = "common"
    verbose_name = "Diverse"
