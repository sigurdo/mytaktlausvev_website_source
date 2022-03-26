from django.apps import AppConfig
from watson import search


class MinutesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "minutes"
    verbose_name = "referat"

    def ready(self):
        search.register(
            self.get_model("Minutes"),
            fields=("title", "content"),
            store=("created", "created_by__username", "created_by__slug"),
        )
