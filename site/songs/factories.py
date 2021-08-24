import factory
from accounts.factories import UserFactory
from .models import Song


class SongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Song

    title = "Song"
    content = "Lyrics"
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
