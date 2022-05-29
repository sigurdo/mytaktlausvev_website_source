from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_event_feed_absolute_url(context):
    return context.request.build_absolute_uri(
        f'{reverse("events:EventFeed")}?token={context.request.user.calendar_feed_token}'
    )
