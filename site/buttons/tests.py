from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from common.mixins import TestMixin
from common.test_utils import test_image_gif_2x2 as test_image


class ButtonsViewTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.test_data = {
            "images": test_image(),
            "num_of_each": 1,
            "button_diameter_mm": 67,
        }

    def test_get_do_not_require_login(self):
        response = self.client.get(reverse("buttons:ButtonsView"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_do_not_require_login(self):
        response = self.client.post(
            reverse("buttons:ButtonsView"),
            self.test_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_returns_pdf(self):
        response = self.client.post(
            reverse("buttons:ButtonsView"),
            self.test_data,
        )
        self.assertEqual(response["content-type"], "application/pdf")

    def test_max_64_of_each(self):
        response = self.client.post(
            reverse("buttons:ButtonsView"),
            {**self.test_data, "num_of_each": 65},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(response["content-type"], "application/pdf")

    def test_max_64_images(self):
        response = self.client.post(
            reverse("buttons:ButtonsView"),
            {
                **self.test_data,
                "images": [test_image() for _ in range(65)],
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotEqual(response["content-type"], "application/pdf")
