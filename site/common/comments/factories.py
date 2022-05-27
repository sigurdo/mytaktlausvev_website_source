from django.contrib.contenttypes.models import ContentType
from factory import LazyAttribute, SelfAttribute, SubFactory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Comment


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    object_pk = SelfAttribute("content_object.id")
    content_type = LazyAttribute(
        lambda comment: ContentType.objects.get_for_model(comment.content_object)
    )
    comment = "This is a comment."
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
