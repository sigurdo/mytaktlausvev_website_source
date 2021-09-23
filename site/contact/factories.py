import factory
from .models import ContactCategory


class ContactCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactCategory

    name = factory.sequence(lambda n: f"Name #{n}")
    email = "styret@taktlaus.no"
