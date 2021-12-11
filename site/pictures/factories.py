from factory.django import DjangoModelFactory, ImageField
from factory import SubFactory
from accounts.factories import UserFactory
from .models import Gallery, Image


class GalleryFactory(DjangoModelFactory):
    class Meta:
        model = Gallery

    title = "Medaljegalla 2291"
    content = "Still going strong!"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    gallery = SubFactory(GalleryFactory)
    image = ImageField(color="blue")
    description = "A most famous image of the color blue."
