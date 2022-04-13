from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data
from storage.forms import StorageAccessUpdateFormset


class StorageAccessTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("storage:StorageAccess")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "accounts.view_storage_access",
        )


class StorageAccessUpdateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("storage:StorageAccessUpdate")

    def post(self):
        return self.client.post(
            self.get_url(),
            {
                **create_formset_post_data(
                    StorageAccessUpdateFormset,
                    total_forms=0,
                    initial_forms=0,
                ),
            },
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """
        Should require permissions for viewing and editing storage access.
        """
        self.assertPermissionRequired(
            self.get_url(),
            "accounts.view_storage_access",
            "accounts.edit_storage_access",
        )

    def test_redirects_to_storage_access_view(self):
        """Should redirect to the storage access view."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(),
            {
                **create_formset_post_data(
                    StorageAccessUpdateFormset,
                    total_forms=0,
                    initial_forms=0,
                ),
            },
        )
        self.assertRedirects(response, reverse("storage:StorageAccess"))
