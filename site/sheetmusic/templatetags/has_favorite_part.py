from django import template

from ..models import FavoritePart

register = template.Library()


@register.simple_tag(takes_context=True)
def has_favorite_part(context, score):
    """Returns True if the user has a favorite part for score."""
    return FavoritePart.objects.filter(
        part__pdf__score=score, user=context["user"]
    ).exists()
