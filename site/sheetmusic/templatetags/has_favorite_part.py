from django import template

from ..models import FavoritePart

register = template.Library()


@register.simple_tag()
def has_favorite_part(user, score):
    """Returns True if the user has a favorite part for score."""
    return FavoritePart.objects.filter(part__pdf__score=score, user=user).exists()
