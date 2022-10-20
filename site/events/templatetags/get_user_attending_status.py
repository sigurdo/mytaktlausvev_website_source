from django import template

from events.models import Attendance

register = template.Library()


@register.simple_tag
def translate_attending_status(status):
    if status == Attendance.ATTENDING:
        return Attendance.ATTENDING.label
    elif status == Attendance.ATTENDING_MAYBE:
        return Attendance.ATTENDING_MAYBE.label
    elif status == Attendance.ATTENDING_NOT:
        return Attendance.ATTENDING_NOT.label
    return "Du har ikkje svart"
