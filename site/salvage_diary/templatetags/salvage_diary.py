from django import template

from salvage_diary.models import Mascot

register = template.Library()


@register.simple_tag
def user_is_creator(mascot: Mascot, user):
    """Returns true if user is part of the mascot creators"""
    return mascot.creators.filter(username=user.username).exists()
