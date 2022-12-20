from factory import SubFactory, post_generation, sequence
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import (
    Instrument,
    InstrumentGroup,
    InstrumentLocation,
    InstrumentType,
    InstrumentTypeDetectionException,
    InstrumentTypeDetectionKeyword,
)


class InstrumentGroupFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentGroup

    name = sequence(lambda n: f"Instrumentgruppe #{n}")


class InstrumentTypeFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentType

    name = sequence(lambda n: f"Instrumenttype #{n}")
    group = SubFactory(InstrumentGroupFactory)

    @post_generation
    def detection_keywords(self, create, detection_keyword_list):
        if not create or not detection_keyword_list:
            return

        self.detection_keywords.set(
            [
                InstrumentTypeDetectionKeywordFactory(
                    keyword=keyword, instrument_type=self
                )
                for keyword in detection_keyword_list
            ]
        )

    @post_generation
    def detection_exceptions(self, create, detection_exception_list):
        if not create or not detection_exception_list:
            return

        self.detection_exceptions.set(
            [
                InstrumentTypeDetectionExceptionFactory(
                    exception=exception, instrument_type=self
                )
                for exception in detection_exception_list
            ]
        )


class InstrumentTypeDetectionKeywordFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentTypeDetectionKeyword

    keyword = sequence(lambda n: f"Instrumenttypeattkjenningnykelord #{n}")
    instrument_type = SubFactory(InstrumentTypeFactory)


class InstrumentTypeDetectionExceptionFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentTypeDetectionException

    exception = sequence(lambda n: f"Instrumenttypeattkjenningunntak #{n}")
    instrument_type = SubFactory(InstrumentTypeFactory)


class InstrumentLocationFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentLocation

    name = sequence(lambda n: f"Instrumentstad #{n}")


class InstrumentFactory(DjangoModelFactory):
    class Meta:
        model = Instrument

    type = SubFactory(InstrumentTypeFactory)
    identifier = sequence(lambda n: n)
    user = None
    location = SubFactory(InstrumentLocationFactory)
    serial_number = "abc-123"
    comment = ""
    state = Instrument.State.OK
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
