from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Choice, Poll, Vote


class PollFactory(DjangoModelFactory):
    class Meta:
        model = Poll

    question = "Best easter egg?"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)


class ChoiceFactory(DjangoModelFactory):
    class Meta:
        model = Choice

    text = "This one"
    poll = SubFactory(PollFactory)


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    choice = SubFactory(ChoiceFactory)
    user = SubFactory(UserFactory)
