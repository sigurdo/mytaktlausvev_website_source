from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentCreateForm

register = template.Library()


@register.inclusion_tag("comments/comment_list.html", takes_context=True)
def comment_list(context, model):
    content_object_data = {
        "content_type": ContentType.objects.get_for_model(model),
        "object_pk": model.pk,
    }
    return {
        "comments": Comment.objects.filter(**content_object_data),
        "form": CommentCreateForm(initial=content_object_data),
        "user": context.request.user,
        "perms": context.get("perms"),
    }
