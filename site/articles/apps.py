from django.apps import AppConfig
from watson import search


class ArticlesConfig(AppConfig):
    name = "articles"
    verbose_name = "artiklar"

    def ready(self):
        search.register(
            self.get_model("Article"),
            fields=("title", "content"),
            store=("created", "created_by__username", "created_by__slug"),
        )
