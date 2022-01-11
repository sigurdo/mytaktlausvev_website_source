from django import template
from django.db.models.query_utils import Q

from authentication.forms import LoginForm
from polls.models import Poll

register = template.Library()


@register.inclusion_tag("sidebar/sidebar.html", takes_context=True)
def sidebar(context):
    poll_filter = Q(public=True) if not context["user"].is_authenticated else Q()
    try:
        poll = Poll.objects.filter(poll_filter).latest()
    except Poll.DoesNotExist:
        poll = None

    return {"user": context["user"], "form_login": LoginForm, "poll": poll}
