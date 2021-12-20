from django import template
from ..models import EventAttendance

register = template.Library()

@register.simple_tag()
def get_event_attendance(user, event):
    return event.get_attendance(user)
