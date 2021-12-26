import factory

from accounts.factories import UserFactory

from .models import Forum, Post, Topic


class ForumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Forum

    title = "General"
    description = "For general stuff."


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    title = "Read only?"
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    forum = factory.SubFactory(ForumFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    content = "A treatise on the applicability, in finite, constrained spaces, of."
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    topic = factory.SubFactory(TopicFactory)
