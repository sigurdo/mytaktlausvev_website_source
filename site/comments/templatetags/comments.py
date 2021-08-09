from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment

register = template.Library()


@register.inclusion_tag("comments/comment_list.html")
def comment_list(model):
    return {
        "comments": Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(model), object_pk=model.pk
        )
    }
