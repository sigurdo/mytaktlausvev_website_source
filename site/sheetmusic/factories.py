from factory.django import DjangoModelFactory
from factory import SubFactory

from accounts.factories import UserFactory
from common.test_utils import test_pdf

from .models import Score, Pdf, Part, UsersPreferredPart


class ScoreFactory(DjangoModelFactory):
    class Meta:
        model = Score

    title = "Score"


class PdfFactory(DjangoModelFactory):
    class Meta:
        model = Pdf

    score = SubFactory(ScoreFactory)
    file = test_pdf()


class PartFactory(DjangoModelFactory):
    class Meta:
        model = Part

    name = "Part"
    pdf = SubFactory(PdfFactory)
    from_page = 1
    to_page = 1


class UsersPreferredPartFactory(DjangoModelFactory):
    class Meta:
        model = UsersPreferredPart

    user = SubFactory(UserFactory)
    part = SubFactory(PartFactory)
