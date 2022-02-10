from django import template
from django.contrib.contenttypes.models import ContentType

from ..forms import CommentCreateForm
from ..models import Comment

register = template.Library()


@register.inclusion_tag("comments/comment_list.html", takes_context=True)
def comment_list(context, model, forum_posts=False):
    content_object_data = {
        "content_type": ContentType.objects.get_for_model(model),
        "object_pk": model.pk,
    }
    form = CommentCreateForm(initial=content_object_data)
    if forum_posts:
        form.fields["comment"].label = "Innlegg"
        form.helper.inputs[0].value = "Legg ut innlegg"
    return {
        "comments": Comment.objects.filter(**content_object_data),
        "form": form,
        "user": context.request.user,
        "perms": context.get("perms"),
        "forum_posts": forum_posts,
    }
