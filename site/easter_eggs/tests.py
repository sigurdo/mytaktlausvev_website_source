from django.test import TestCase
from django.urls import reverse

from common.mixins import TestMixin


class BrewViewTestSuite(TestMixin, TestCase):
    def test_returns_418(self):
        response = self.client.post(
            reverse("easter_eggs:BrewView"), {"drink": "coffee"}
        )
        self.assertEqual(response.status_code, 418)


class EasterEggButtonTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("easter_eggs:EasterEggButton")

    def test_returns_pdf(self):
        response = self.client.get(
            self.get_url(),
        )
        self.assertEqual(response["content-type"], "application/pdf")
