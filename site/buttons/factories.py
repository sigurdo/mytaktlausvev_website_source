from factory import SubFactory, sequence
from factory.django import DjangoModelFactory, ImageField

from accounts.factories import UserFactory

from .models import ButtonDesign


class ButtonDesignFactory(DjangoModelFactory):
    class Meta:
        model = ButtonDesign

    name = sequence(lambda n: f"Button #{n}")
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
    image = ImageField(color="red")
