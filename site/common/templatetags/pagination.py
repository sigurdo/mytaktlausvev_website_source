from django import template

register = template.Library()


@register.simple_tag
def get_elided_page_range(paginator, page_number, on_each_side=2, on_ends=1):
    return paginator.get_elided_page_range(
        number=page_number, on_each_side=on_each_side, on_ends=on_ends
    )
