from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Minutes


class MinutesFactory(DjangoModelFactory):
    class Meta:
        model = Minutes

    title = "Board Meeting"
    content = "Talk, talk, talk."
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
