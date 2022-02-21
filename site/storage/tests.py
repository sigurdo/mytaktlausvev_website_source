from django.test import TestCase
from django.urls import reverse

from common.mixins import TestMixin

class StorageAccessViewTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("storage:StorageAccessView")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())
    
    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "common.view_storage_access",
        )
