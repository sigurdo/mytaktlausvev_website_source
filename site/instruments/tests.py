from django.test import TestCase

from common.mixins import TestMixin

from .factories import InstrumentTypeFactory


class InstrumentTypeTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_type = InstrumentTypeFactory(name="Tuba")

    def test_to_str(self):
        self.assertEqual(str(self.instrument_type), "Tuba")
