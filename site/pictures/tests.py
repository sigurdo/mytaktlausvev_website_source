from datetime import date
from django.test import TestCase
from django.utils.text import slugify
from common.mixins import TestMixin
from .factories import GalleryFactory, ImageFactory
from .models import Image


class GalleryTestSuite(TestCase):
    def setUp(self):
        self.gallery = GalleryFactory()

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
