from django import template

register = template.Library()


@register.simple_tag()
def get_event_attendance(user, event):
    return event.get_attendance(user)
