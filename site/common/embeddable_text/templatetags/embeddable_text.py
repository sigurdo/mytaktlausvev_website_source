from django import template

from ..models import EmbeddableText

register = template.Library()


@register.simple_tag
def get_embeddable_text(name):
    text, _ = EmbeddableText.objects.get_or_create(name=name)
    return text.content
