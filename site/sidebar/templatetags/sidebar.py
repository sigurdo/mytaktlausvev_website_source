from django import template

from authentication.forms import LoginForm

register = template.Library()


@register.inclusion_tag("sidebar/sidebar.html", takes_context=True)
def sidebar(context):
    return {"authenticated": context["user"].is_authenticated, "form_login": LoginForm}
