from django.apps import AppConfig
from watson import search


class UserEventsConfig(AppConfig):
    name = "pictures"
    verbose_name = "fotoarkiv"

    def ready(self):
        search.register(
            self.get_model("Gallery"),
            fields=("title", "content"),
            store=("created", "created_by__username", "created_by__slug"),
        )
