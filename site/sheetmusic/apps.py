"""Configuration-file for the 'sheetmusic'-app"""
from django.apps import AppConfig
from watson import search


class SheetmusicConfig(AppConfig):
    """Configuration-class for the 'sheetmusic'-app"""

    name = "sheetmusic"
    verbose_name = "notar"

    def ready(self):
        search.register(
            self.get_model("Score"),
            fields=("title", "content"),
            store=("created", "created_by__username", "created_by__slug"),
        )
