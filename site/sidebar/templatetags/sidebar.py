from django import template
from django.db.models.query_utils import Q

from accounts.forms import ImageSharingConsentForm
from authentication.forms import LoginForm
from polls.models import Poll

register = template.Library()


@register.inclusion_tag("sidebar/sidebar.html")
def sidebar(user, request_path):
    poll_filter = Q(public=True) if not user or not user.is_authenticated else Q()
    try:
        poll = Poll.objects.filter(poll_filter).latest()
    except Poll.DoesNotExist:
        poll = None

    return {
        "user": user,
        "request_path": request_path,
        "form_login": LoginForm(autofocus=False),
        "form_image_sharing_consent": ImageSharingConsentForm(request_path),
        "poll": poll,
    }
