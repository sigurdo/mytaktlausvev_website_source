from django.apps import AppConfig


class EmbeddableTextConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common.embeddable_text"
    verbose_name = "Innbyggbar tekst"
