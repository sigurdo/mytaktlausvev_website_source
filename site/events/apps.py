from django.apps import AppConfig
from watson import search


class UserEventsConfig(AppConfig):
    name = "events"
    verbose_name = "Hendingar"

    def ready(self):
        search.register(
            self.get_model("Event"),
            fields=("title", "content"),
            store=("created", "created_by__username", "created_by__slug"),
        )
