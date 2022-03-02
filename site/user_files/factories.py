from factory import SubFactory
from factory.django import DjangoModelFactory, FileField

from accounts.factories import UserFactory

from .models import File


class FileFactory(DjangoModelFactory):
    class Meta:
        model = File

    name = "Free World Fantasy"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
    file = FileField(filename="Free World Fantasy.mp3")
