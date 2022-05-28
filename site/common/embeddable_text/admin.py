from django.contrib.admin import site

from .models import EmbeddableText

site.register(EmbeddableText)
