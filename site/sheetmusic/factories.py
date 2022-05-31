from factory import SubFactory, sequence
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from common.test_utils import test_pdf
from instruments.factories import InstrumentTypeFactory

from .models import FavoritePart, Part, Pdf, Score


class ScoreFactory(DjangoModelFactory):
    class Meta:
        model = Score

    title = sequence(lambda n: f"Score #{n}")
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)


class PdfFactory(DjangoModelFactory):
    class Meta:
        model = Pdf

    score = SubFactory(ScoreFactory)
    file = test_pdf()
    filename_original = test_pdf().name


class PartFactory(DjangoModelFactory):
    class Meta:
        model = Part

    instrument_type = SubFactory(InstrumentTypeFactory)
    part_number = sequence(lambda n: n)
    note = ""
    pdf = SubFactory(PdfFactory)
    from_page = 1
    to_page = 1


class FavoritePartFactory(DjangoModelFactory):
    class Meta:
        model = FavoritePart

    user = SubFactory(UserFactory)
    part = SubFactory(PartFactory)
