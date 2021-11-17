from http import HTTPStatus
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http.response import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectMixin
from accounts.factories import UserFactory, SuperUserFactory
from articles.views import SlugPathMixin
from common.mixins import TestMixin


def test_image():
    """Returns a temporary image file that can be used in tests."""
    gif = b"GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;"
    return SimpleUploadedFile(
        name="test_image.gif",
        content=gif,
        content_type="image/gif",
    )

class ButtonsTestCase(TestMixin, TestCase):
    def test_get_do_not_require_login(self):
        response = self.client.get(reverse("buttons:buttons"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    # def test_post_do_not_require_login(self):
    #     response = self.client.post(reverse("buttons:buttons"), {"images": test_image(), "num_of_each": 1})
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.assertEqual(response["content-type"], "application/pdf")
