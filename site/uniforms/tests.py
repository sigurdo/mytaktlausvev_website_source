from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data

from .factories import JacketFactory, JacketLocationFactory
from .forms import JacketsUpdateFormset
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
            formset_class=JacketsUpdateFormset,
            data=self.formset_post_data,
            total_forms=1 + num_of_new,
            initial_forms=1,
        )

    def setUp(self):
        self.user = UserFactory()
        self.jacket = JacketFactory(owner=self.user)
        self.formset_post_data = [
            {
                "number": self.jacket.number,
                "comment": self.jacket.comment,
                "state": self.jacket.state,
                "owner": self.jacket.owner.pk,
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
        owner = UserFactory()
        location = JacketLocationFactory()
        self.formset_post_data.append(
            {
                "number": number,
                "comment": comment,
                "state": state,
                "owner": owner.pk,
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
        self.assertEqual(jacket.owner, owner)
        self.assertEqual(jacket.location, location)

    def test_update_jacket(self):
        number = self.jacket.number + 10
        comment = "mangler en knapp"
        state = Jacket.State.GOOD
        owner = UserFactory()
        location = JacketLocationFactory()
        self.formset_post_data[0]["number"] = number
        self.formset_post_data[0]["comment"] = comment
        self.formset_post_data[0]["state"] = state
        self.formset_post_data[0]["owner"] = owner.pk
        self.formset_post_data[0]["location"] = location.pk
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(Jacket.objects.count(), 1)
        jacket = Jacket.objects.last()
        self.assertEqual(jacket.number, number)
        self.assertEqual(jacket.comment, comment)
        self.assertEqual(jacket.state, state)
        self.assertEqual(jacket.owner, owner)
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
            "uniforms.change_jacket",
            "accounts.change_usercustom",
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

    def post(self, user, set_owner=False, remove_old_ownerships=False):
        self.client.force_login(SuperUserFactory())
        return self.client.post(
            self.get_url(),
            {
                "user": user.pk,
                "set_owner": set_owner,
                "remove_old_ownerships": remove_old_ownerships,
            },
        )

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(), "uniforms.change_jacket", "accounts.change_usercustom"
        )

    def test_add_user(self):
        user = UserFactory()
        self.post(user)
        user.refresh_from_db()
        self.jacket.refresh_from_db()
        self.assertEqual(user.jacket, self.jacket)
        self.assertEqual(self.jacket.owner, None)

    def test_add_user_set_owner(self):
        user = UserFactory()
        self.post(user, set_owner=True)
        user.refresh_from_db()
        self.jacket.refresh_from_db()
        self.assertEqual(user.jacket, self.jacket)
        self.assertEqual(self.jacket.owner, user)

    def test_add_user_remove_old_ownerships(self):
        user = UserFactory()
        self.jacket.owner = user
        self.jacket.save()
        other_jacket = JacketFactory(owner=user)
        self.post(user, remove_old_ownerships=True)
        user.refresh_from_db()
        self.jacket.refresh_from_db()
        other_jacket.refresh_from_db()
        self.assertEqual(user.jacket, self.jacket)
        self.assertEqual(self.jacket.owner, None)
        self.assertEqual(other_jacket.owner, None)

    def test_add_user_set_owner_remove_old_ownerships(self):
        user = UserFactory()
        self.jacket.owner = user
        self.jacket.save()
        other_jacket = JacketFactory(owner=user)
        self.post(user, set_owner=True, remove_old_ownerships=True)
        user.refresh_from_db()
        self.jacket.refresh_from_db()
        other_jacket.refresh_from_db()
        self.assertEqual(user.jacket, self.jacket)
        self.assertEqual(self.jacket.owner, user)
        self.assertEqual(other_jacket.owner, None)


class RemoveJacketUserTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.jacket = JacketFactory()
        self.user = UserFactory(jacket=self.jacket)
        self.jacket.owner = self.user
        self.jacket.save()

    def get_url(self):
        return reverse(
            "uniforms:RemoveJacketUser", args=[self.jacket.number, self.user.slug]
        )

    def post(self, remove_owner=False):
        self.client.force_login(SuperUserFactory())
        return self.client.post(self.get_url(), {"remove_owner": remove_owner})

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(), "uniforms.change_jacket", "accounts.change_usercustom"
        )

    def test_remove_user(self):
        self.post()
        self.jacket.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.jacket.owner, self.user)
        self.assertEqual(self.user.jacket, None)

    def test_remove_user_remove_owner(self):
        self.post(remove_owner=True)
        self.jacket.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.jacket.owner, None)
        self.assertEqual(self.user.jacket, None)

    def test_remove_user_not_remove_other_owner(self):
        owner = UserFactory()
        self.jacket.owner = owner
        self.jacket.save()
        self.post(remove_owner=True)
        self.jacket.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.jacket.owner, owner)
        self.assertEqual(self.user.jacket, None)
