from django.apps import AppConfig
from watson import search


class PollsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"
    verbose_name = "avstemmingar"

    def ready(self):
        search.register(
            self.get_model("Poll"),
            fields=("question",),
            store=("created", "created_by__username", "created_by__slug"),
        )
