from django import template

register = template.Library()

@register.inclusion_tag("quotes/quote.html")
def show_quote(quote):
    return {'quote': quote}
