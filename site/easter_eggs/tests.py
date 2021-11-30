from django.test import TestCase
from django.urls import reverse
from common.mixins import TestMixin


class BrewViewTestSuite(TestMixin, TestCase):
    def test_returns_418(self):
        response = self.client.post(
            reverse("easter_eggs:BrewView"), {"drink": "coffee"}
        )
        self.assertEqual(response.status_code, 418)
