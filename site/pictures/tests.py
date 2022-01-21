from datetime import date
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.datastructures import MultiValueDict
from django.utils.text import slugify

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data, test_image, test_pdf
from pictures.forms import ImageCreateForm, ImageFormSet

from .factories import GalleryFactory, ImageFactory
from .models import Gallery, Image


class GalleryTestSuite(TestCase):
    def setUp(self):
        self.gallery = GalleryFactory()

    def test_get_absolute_url(self):
        """Should link to the gallery's detail page."""
        self.assertEqual(
            self.gallery.get_absolute_url(),
            reverse("pictures:GalleryDetail", args=[self.gallery.slug]),
        )

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.gallery.slug, slugify(self.gallery.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.gallery.slug
        self.gallery.title = "Different title"
        self.gallery.save()
        self.assertEqual(self.gallery.slug, slug_before)

    def test_slug_unique(self):
        """Should create unique slugs."""
        gallery_same_title = GalleryFactory(title=self.gallery.title)
        self.assertNotEqual(self.gallery.slug, gallery_same_title.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        article = GalleryFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(article.slug, slug)

    def test_default_date_is_current_date(self):
        """The default date should be the current date."""
        self.assertEqual(self.gallery.date, date.today())


class ImageTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.image = ImageFactory()

    def test_to_str(self):
        """`__str__` should be the image filename."""
        self.assertTrue(str(self.image), self.image.image.name)

    def test_get_absolute_url(self):
        """Should be the image's URL."""
        self.assertTrue(self.image.get_absolute_url(), self.image.image.url)

    def test_deleting_gallery_deletes_its_images(self):
        """Deleting a gallery should delete all images in the gallery."""
        self.assertTrue(Image.objects.all().exists())
        self.image.gallery.delete()
        self.assertFalse(Image.objects.all().exists())

    def test_deleting_image_deletes_file_on_disk(self):
        """Deleting an image should delete the image file on the disk."""
        pass


class ImageCreateFormTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.gallery = GalleryFactory()

    def test_saves_all_uploaded_images(self):
        form = ImageCreateForm(
            gallery=self.gallery,
            files=MultiValueDict({"image": [test_image() for _ in range(3)]}),
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Image.objects.count(), 3)

    def test_error_if_one_or_more_files_are_not_images(self):
        """Should add a form error if one or more files are not images."""
        form = ImageCreateForm(
            gallery=self.gallery,
            files=MultiValueDict(
                {"image": [test_image() for _ in range(3)] + [test_pdf()]}
            ),
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last opp eit gyldig bilete. Fila du lasta opp var ødelagt eller ikkje eit bilete.",
            form.errors["image"],
        )


class GalleryDetailTestSuite(TestMixin, TestCase):
    def test_queryset_excludes_galleries_with_no_images(self):
        """Should exclude galleries with no images."""
        pass


class GalleryCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.gallery_data = {
            "title": "A Title",
            "date": "2021-11-25",
            "content": "Gallery text",
        }

    def get_url(self) -> str:
        return reverse("pictures:GalleryCreate")

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.gallery_data)

        self.assertEqual(Gallery.objects.count(), 1)
        gallery = Gallery.objects.last()
        self.assertEqual(gallery.created_by, user)
        self.assertEqual(gallery.modified_by, user)

    def test_success_redirect(self):
        """Should redirect to the view for uploading images on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url(), self.gallery_data)
        self.assertEqual(Gallery.objects.count(), 1)
        gallery = Gallery.objects.last()
        self.assertRedirects(
            response, reverse("pictures:ImageCreate", args=[gallery.slug])
        )


class ImageCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.gallery = GalleryFactory()
        self.image_data = {"image": test_image()}

    def get_url(self, slug=None) -> str:
        return reverse("pictures:ImageCreate", args=[slug or self.gallery.slug])

    def test_404_if_gallery_not_found(self):
        """Should return a 404 if the gallery isn't found."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url("gallery-not-exist"))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_adds_gallery_to_context_data(self):
        """Should add the gallery to the context data."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.context["gallery"], self.gallery)

    def test_error_if_uploaded_file_is_not_image(self):
        """Should show a form error if the uploaded file isn't an image."""
        self.image_data["image"] = test_pdf()
        self.client.force_login(UserFactory())
        response = self.client.post(self.get_url(), self.image_data)
        self.assertFormError(
            response,
            "form",
            "image",
            "Last opp eit gyldig bilete. Fila du lasta opp var ødelagt eller ikkje eit bilete.",
        )

    def test_error_if_one_or_more_files_are_not_images(self):
        """
        Should show a form error if one or more
        of the uploaded files are not images.
        """
        self.image_data["image"] = [test_pdf(), test_image()]
        self.client.force_login(UserFactory())
        response = self.client.post(self.get_url(), self.image_data)
        self.assertFormError(
            response,
            "form",
            "image",
            "Last opp eit gyldig bilete. Fila du lasta opp var ødelagt eller ikkje eit bilete.",
        )

    def test_success_redirect(self):
        """Should redirect to the view for updating a gallery on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url(), self.image_data)
        self.assertRedirects(
            response, reverse("pictures:GalleryUpdate", args=[self.gallery.slug])
        )


class GalleryUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.gallery = GalleryFactory()
        self.gallery_data = {
            "title": "A Title",
            "date": "2021-11-25",
            "content": "Gallery text",
            **create_formset_post_data(
                formset_class=ImageFormSet,
                initial_forms=0,
                total_forms=0,
            ),
        }

    def get_url(self):
        """Returns the URL for the gallery update view for `self.gallery`."""
        return reverse("pictures:GalleryUpdate", args=[self.gallery.slug])

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating gallery."""
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.gallery_data)

        created_by_previous = self.gallery.created_by
        self.gallery.refresh_from_db()
        self.assertEqual(self.gallery.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.gallery_data)

        self.gallery.refresh_from_db()
        self.assertEqual(self.gallery.modified_by, user)
