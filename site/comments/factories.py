import factory
from django.contrib.contenttypes.models import ContentType

from accounts.factories import UserFactory

from .models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    object_pk = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda comment: ContentType.objects.get_for_model(comment.content_object)
    )
    comment = "This is a comment."
    created_by = factory.SubFactory(UserFactory)
