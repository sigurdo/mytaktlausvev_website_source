from factory import SubFactory, sequence
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Jacket, JacketLocation, JacketUser


class JacketLocationFactory(DjangoModelFactory):
    class Meta:
        model = JacketLocation
        django_get_or_create = ["name"]

    name = "Jakkeskapet"


class JacketFactory(DjangoModelFactory):
    class Meta:
        model = Jacket

    number = sequence(lambda n: 1 + n)
    location = SubFactory(JacketLocationFactory)
    comment = ""
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)


class JacketUserFactory(DjangoModelFactory):
    class Meta:
        model = JacketUser

    user = SubFactory(UserFactory)
    jacket = SubFactory(JacketFactory)
    is_owner = True
