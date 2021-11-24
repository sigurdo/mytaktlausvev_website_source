import factory
from accounts.factories import UserFactory
from .models import Julekalender, Window


class JulekalenderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Julekalender

    year = factory.sequence(lambda n: 2030 + n)


class WindowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Window

    calendar = factory.SubFactory(JulekalenderFactory)
    index = factory.sequence(lambda n: n)

    title = "Another window"
    content = "And the story repeats..."
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
