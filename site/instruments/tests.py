from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data

from .factories import (
    InstrumentFactory,
    InstrumentGroupFactory,
    InstrumentLocationFactory,
)
from .forms import InstrumentUpdateFormset
from .models import Instrument


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

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())


class InstrumentsUpdateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentsUpdate")

    def create_post_data(self, num_of_new=0):
        return create_formset_post_data(
            formset_class=InstrumentUpdateFormset,
            data=self.formset_data,
            total_forms=1 + num_of_new,
            initial_forms=1,
        )

    def setUp(self):
        self.instrument = InstrumentFactory(name="Bassklarinett")
        self.formset_data = [
            {
                "name": self.instrument.name,
                "group": self.instrument.group.pk,
                "user": "",
                "location": self.instrument.location.pk,
                "serial_number": self.instrument.serial_number,
                "comment": self.instrument.comment,
                "state": self.instrument.state,
                "id": self.instrument.pk,
            }
        ]

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "instruments.add_instrument",
            "instruments.change_instrument",
            "instruments.delete_instrument",
        )

    def test_create_instrument(self):
        group = InstrumentGroupFactory()
        location = InstrumentLocationFactory()
        self.formset_data.append(
            {
                "name": "Klarinett 14",
                "group": group.pk,
                "location": location.pk,
                "state": Instrument.State.GOOD,
            }
        )
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data(num_of_new=1))
        self.assertEqual(Instrument.objects.count(), 2)

    def test_update_instrument(self):
        user = UserFactory()
        self.formset_data[0]["name"] = "Bassklarinett 1"
        self.formset_data[0]["user"] = user.pk
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data())
        self.instrument.refresh_from_db()
        self.assertEqual(self.instrument.name, "Bassklarinett 1")
        self.assertEqual(self.instrument.user, user)

    def test_delete_instrument(self):
        self.formset_data[0]["DELETE"] = "on"
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(Instrument.objects.count(), 0)
