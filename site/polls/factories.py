import factory

from accounts.factories import UserFactory

from .models import Choice, Poll


class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poll

    question = "Best easter egg?"
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    text = "This one"
    poll = factory.SubFactory(PollFactory)
