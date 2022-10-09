from http import HTTPStatus

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data

from .factories import JacketFactory, JacketLocationFactory
from .forms import JacketsFormset
from .models import Jacket


class JacketTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.jacket = JacketFactory(number=42)

    def test_to_str(self):
        self.assertEqual(str(self.jacket), "Jakke 42")

    def test_number_unique(self):
        with self.assertRaises(IntegrityError):
            JacketFactory(number=42)

    def test_delete_location_restricted(self):
        with self.assertRaises(IntegrityError):
            self.jacket.location.delete()

    def test_jacket_state_defaults_to_good(self):
        """A jacket's `state` should default to `GOOD`."""
        self.assertEqual(self.jacket.state, Jacket.State.GOOD)


class JacketLocationTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.jacket_location = JacketLocationFactory(name="Hjemme")

    def test_to_str(self):
        self.assertEqual(str(self.jacket_location), "Hjemme")


class JacketListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("uniforms:JacketList")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())


class JacketsUpdateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("uniforms:JacketsUpdate")

    def create_post_data(self, num_of_new=0):
        return create_formset_post_data(
            JacketsFormset,
            data=self.formset_post_data,
            total_forms=1 + num_of_new,
            initial_forms=1,
        )

    def setUp(self):
        self.jacket = JacketFactory()
        self.formset_post_data = [
            {
                "number": self.jacket.number,
                "comment": self.jacket.comment,
                "state": self.jacket.state,
                "location": self.jacket.location.pk,
                "id": self.jacket.pk,
            }
        ]

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "uniforms.add_jacket",
            "uniforms.change_jacket",
            "uniforms.delete_jacket",
        )

    def test_create_jacket(self):
        number = self.jacket.number + 1
        comment = "mangler en knapp"
        state = Jacket.State.GOOD
        location = JacketLocationFactory()
        self.formset_post_data.append(
            {
                "number": number,
                "comment": comment,
                "state": state,
                "location": location.pk,
            }
        )
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data(num_of_new=1))
        self.assertEqual(Jacket.objects.count(), 2)
        jacket = Jacket.objects.last()
        self.assertEqual(jacket.number, number)
        self.assertEqual(jacket.comment, comment)
        self.assertEqual(jacket.state, state)
        self.assertEqual(jacket.location, location)

    def test_update_jacket(self):
        number = self.jacket.number + 10
        comment = "mangler en knapp"
        state = Jacket.State.GOOD
        location = JacketLocationFactory()
        self.formset_post_data[0]["number"] = number
        self.formset_post_data[0]["comment"] = comment
        self.formset_post_data[0]["state"] = state
        self.formset_post_data[0]["location"] = location.pk
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(Jacket.objects.count(), 1)
        jacket = Jacket.objects.last()
        self.assertEqual(jacket.number, number)
        self.assertEqual(jacket.comment, comment)
        self.assertEqual(jacket.state, state)
        self.assertEqual(jacket.location, location)

    def test_delete_jacket(self):
        self.formset_post_data[0]["DELETE"] = "on"
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(Jacket.objects.count(), 0)


