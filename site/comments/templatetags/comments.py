from django import template
from django.contrib.contenttypes.models import ContentType
from crispy_forms.utils import render_crispy_form
from ..models import Comment
from ..forms import CommentCreateForm

register = template.Library()


@register.inclusion_tag("comments/comment_list.html", takes_context=True)
def comment_list(context, model):
    return {
        "comments": Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(model), object_pk=model.pk
        ),
        "authenticated": context.request.user.is_authenticated,
    }


@register.inclusion_tag("comments/comment_form.html")
def comment_form(model):
    return {
        "form": CommentCreateForm(
            initial={
                "content_type": ContentType.objects.get_for_model(model),
                "object_pk": model.pk,
            }
        )
    }
