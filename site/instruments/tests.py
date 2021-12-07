from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from common.mixins import TestMixin

from .factories import (
    InstrumentGroupFactory,
    InstrumentLocationFactory,
    InstrumentFactory,
)


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


class InstrumentListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentList")

    def setUp(self):
        pass

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())


class InstrumentsUpdateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentsUpdate")

    def setUp(self):
        pass

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "instruments.add_instrument",
            "instruments.change_instrument",
            "instruments.delete_instrument",
        )
