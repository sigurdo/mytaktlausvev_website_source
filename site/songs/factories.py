import factory
from accounts.factories import UserFactory
from .models import Song


class SongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Song

    title = "Song"
    description = "Lyrics"
    created_by = factory.SubFactory(UserFactory)
