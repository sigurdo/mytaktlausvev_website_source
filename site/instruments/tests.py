from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from common.mixins import TestMixin

from .factories import InstrumentGroupFactory, InstrumentLocationFactory, InstrumentFactory


class InstrumentGroupTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_group = InstrumentGroupFactory(name="Tuba")

    def test_to_str(self):
        self.assertEqual(str(self.instrument_group), "Tuba")


class InstrumentLocationTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_location = InstrumentLocationFactory(name="Lager")

    def test_to_str(self):
        self.assertEqual(str(self.instrument_location), "Lager")


class InstrumentTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument = InstrumentFactory(name="Tuba 1")

    def test_to_str(self):
        self.assertEqual(str(self.instrument), "Tuba 1")
    
    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            InstrumentFactory(name="Tuba 1")
