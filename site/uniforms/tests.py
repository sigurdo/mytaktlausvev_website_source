from http import HTTPStatus

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data

from .factories import JacketFactory, JacketLocationFactory, JacketUserFactory
from .forms import JacketsUpdateFormset
from .models import Jacket, JacketUser


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


class JacketUserTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.jacket = JacketFactory(number=42)
        self.user = UserFactory(name="Mikkel Jakkeson")
        self.jacket_user = JacketUserFactory(jacket=self.jacket, user=self.user)

    def test_to_str(self):
        self.assertEqual(str(self.jacket_user), "Mikkel Jakkeson - Jakke 42")

    def test_max_one_owner_per_jacket(self):
        JacketUserFactory(jacket=self.jacket, is_owner=False)
        with self.assertRaises(IntegrityError):
            JacketUserFactory(jacket=self.jacket, is_owner=True)

    def test_max_one_jacket_per_user(self):
        with self.assertRaises(IntegrityError):
            JacketUserFactory(user=self.user)


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
            JacketsUpdateFormset,
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


class JacketUsersTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.jacket = JacketFactory()

    def get_url(self):
        return reverse("uniforms:JacketUsers", args=[self.jacket.number])

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "uniforms.add_jacketuser",
            "uniforms.change_jacketuser",
            "uniforms.delete_jacketuser",
        )

    def test_jacket_in_context(self):
        self.client.force_login(SuperUserFactory())
        context = self.client.get(self.get_url()).context
        self.assertEqual(context["jacket"], self.jacket)


class AddJacketUserTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.jacket = JacketFactory()

    def get_url(self):
        return reverse("uniforms:AddJacketUser", args=[self.jacket.number])

    def post(self, user, set_owner=False):
        self.client.force_login(SuperUserFactory())
        return self.client.post(
            self.get_url(),
            {
                "user": user.pk,
                "set_owner": set_owner,
            },
        )

    def test_requires_permission(self):
        self.assertPermissionRequired(self.get_url(), "uniforms.add_jacketuser")

    def test_add_user(self):
        user = UserFactory()
        self.post(user)
        jacket_user = JacketUser.objects.get(jacket=self.jacket, user=user)
        self.assertEqual(jacket_user.jacket, self.jacket)
        self.assertEqual(jacket_user.user, user)
        self.assertEqual(jacket_user.is_owner, False)

    def test_add_user_set_owner(self):
        user = UserFactory()
        self.post(user, set_owner=True)
        jacket_user = JacketUser.objects.get(jacket=self.jacket, user=user)
        self.assertEqual(jacket_user.jacket, self.jacket)
        self.assertEqual(jacket_user.user, user)
        self.assertEqual(jacket_user.is_owner, True)


class RemoveJacketUserTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.jacket_user = JacketUserFactory()
        self.jacket = self.jacket_user.jacket
        self.user = self.jacket_user.user

    def get_url(self):
        return reverse(
            "uniforms:RemoveJacketUser", args=[self.jacket.number, self.user.slug]
        )

    def post(self, transfer_ownership=False):
        self.client.force_login(SuperUserFactory())
        return self.client.post(
            self.get_url(), {"transfer_ownership": transfer_ownership}
        )

    def test_requires_permission(self):
        self.assertPermissionRequired(self.get_url(), "uniforms.delete_jacketuser")

    def test_remove_user(self):
        self.post()
        self.assertEqual(
            JacketUser.objects.filter(jacket=self.jacket, user=self.user).exists(),
            False,
        )

    def test_remove_user_transfer_ownership(self):
        extra_jacket_user = JacketUserFactory(jacket=self.jacket, is_owner=False)
        self.post(transfer_ownership=True)
        extra_jacket_user.refresh_from_db()
        self.assertEqual(
            JacketUser.objects.filter(jacket=self.jacket, user=self.user).exists(),
            False,
        )
        self.assertEqual(extra_jacket_user.is_owner, True)

    def test_remove_user_no_transfer_ownership(self):
        extra_jacket_user = JacketUserFactory(jacket=self.jacket, is_owner=False)
        self.post(transfer_ownership=False)
        extra_jacket_user.refresh_from_db()
        self.assertEqual(
            JacketUser.objects.filter(jacket=self.jacket, user=self.user).exists(),
            False,
        )
        self.assertEqual(extra_jacket_user.is_owner, False)


class JacketUserMakeOwnerTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse(
            "uniforms:JacketUserMakeOwner", args=[self.jacket.number, self.user.slug]
        )

    def setUp(self):
        self.jacket_user = JacketUserFactory(is_owner=False)
        self.jacket = self.jacket_user.jacket
        self.user = self.jacket_user.user

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "uniforms.change_jacketuser",
            method="post",
            status_success=HTTPStatus.FOUND,
        )

    def post(self):
        self.client.force_login(SuperUserFactory())
        return self.client.post(self.get_url())

    def test_make_owner(self):
        """Make user owner."""
        self.post()
        self.jacket_user.refresh_from_db()
        self.assertEqual(self.jacket_user.is_owner, True)

    def test_remove_old_owner(self):
        """Make user owner when other user already is owner."""
        old_owner = JacketUserFactory(jacket=self.jacket, is_owner=True)
        self.post()
        self.jacket_user.refresh_from_db()
        old_owner.refresh_from_db()
        self.assertEqual(self.jacket_user.is_owner, True)
        self.assertEqual(old_owner.is_owner, False)
