from factory.django import DjangoModelFactory
from factory import SubFactory
from accounts.factories import UserFactory
from .models import Gallery


class GalleryFactory(DjangoModelFactory):
    class Meta:
        model = Gallery

    title = "Medaljegalla 2291"
    content = "Still going strong!"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
