from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField

from accounts.factories import UserFactory

from .models import ButtonDesign


class ButtonDesignFactory(DjangoModelFactory):
    class Meta:
        model = ButtonDesign

    name = "Taktlausbutton - Raud"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
    image = ImageField(color="red")
