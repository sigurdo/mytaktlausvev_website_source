from http import HTTPStatus

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.factories import SuperUserFactory
from buttons.factories import ButtonDesignFactory
from buttons.models import ButtonDesign
from common.mixins import TestMixin
from common.test_utils import test_image


class ButtonDesignTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.button_design = ButtonDesignFactory()

    def test_name_unique(self):
        """`name` should be unique."""
        with self.assertRaises(IntegrityError):
            ButtonDesignFactory(name=self.button_design.name)

    def test_to_str_is_name(self):
        """`__str__` should equal `name`."""
        self.assertEqual(str(self.button_design), self.button_design.name)

    def test_creates_slug_from_name_automatically(self):
        """Should create a slug from the name automatically during creation."""
        self.assertEqual(self.button_design.slug, slugify(self.button_design.name))

    def test_does_not_update_slug_when_name_is_changed(self):
        """Should not change the slug when the name is changed."""
        slug_before = self.button_design.slug
        self.button_design.name = "Different name"
        self.button_design.save()
        self.assertEqual(self.button_design.slug, slug_before)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        button_design = ButtonDesignFactory(
            name="name that is very different from the slug", slug=slug
        )
        self.assertEqual(button_design.slug, slug)

    def test_ordering(self):
        """Should be ordered by `date`, descending."""
        self.assertModelOrdering(
            ButtonDesign,
            ButtonDesignFactory,
            [
                {"name": "AAA"},
                {"name": "BBB"},
                {"name": "ZZZ"},
            ],
        )


class ButtonsViewTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.test_data = {
            "images": test_image(),
            "num_of_each": 1,
            "button_visible_diameter_mm": 67,
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


class ButtonDesignCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("buttons:ButtonDesignCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            {"name": "Nidaros-SMASH 2023", "image": test_image()},
        )

        self.assertEqual(ButtonDesign.objects.count(), 1)
        button_design = ButtonDesign.objects.last()
        self.assertEqual(button_design.created_by, user)
        self.assertEqual(button_design.modified_by, user)

    def test_success_url_is_buttons_view(self):
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(),
            {"name": "Nidaros-SMASH 2023", "image": test_image()},
        )
        self.assertRedirects(response, reverse("buttons:ButtonsView"))
