from django.apps import AppConfig

# Checks must be imported into a file loaded by Django
from .checks import check_codestyles_exist  # noqa


class CommonConfig(AppConfig):
    name = "common"
