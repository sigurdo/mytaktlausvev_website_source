from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from common.test_utils import test_txt_file

from .factories import FileFactory
from .models import File
from .views import FileList


class FileTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.file = FileFactory()

    def test_get_absolute_url(self):
        """Should link to the serve view for the file."""
        self.assertEqual(
            self.file.get_absolute_url(),
            reverse("user_files:FileServe", args=[self.file.slug]),
        )

    def test_to_str(self):
        """Should equal the file's `name`."""
        self.assertEqual(str(self.file), self.file.name)

    def test_creates_slug_from_name_automatically(self):
        """Should create a slug from the name automatically during creation."""
        self.assertEqual(self.file.slug, slugify(self.file.name))

    def test_does_not_update_slug_when_name_is_changed(self):
        """Should not change the slug when the name is changed."""
        slug_before = self.file.slug
        self.file.name = "Different name"
        self.file.save()
        self.assertEqual(self.file.slug, slug_before)

    def test_creates_unique_slugs(self):
        """Should create unique slugs even if names match."""
        file_same_name = FileFactory(name=self.file.name)
        self.assertNotEqual(self.file.slug, file_same_name.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        file = FileFactory(name="Title that is very different from the slug", slug=slug)
        self.assertEqual(file.slug, slug)

    def test_default_no_public(self):
        """`public` should default to `False`"""
        file = FileFactory()
        self.assertFalse(file.public)


class FileListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("user_files:FileList")

    def test_login_required(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_breadcrumbs(self):
        """
        FileList should have an empty list of breadcrumbs
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(breadcrumbs, [])


class FileServeTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.file = FileFactory()
        self.public_file = FileFactory(public=True)

    def get_url(self, file):
        return reverse("user_files:FileServe", args=[file.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.file))

    def test_public_no_requires_login(self):
        """Public file should not require login."""
        self.client.logout()
        response = self.client.get(self.get_url(self.public_file))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_serves_file(self):
        """Should serve the file."""
        response = self.client.get(self.get_url(self.public_file))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["content-type"], "audio/mpeg")


class FileCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("user_files:FileCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            {"name": "616.mp3", "file": test_txt_file()},
        )

        self.assertEqual(File.objects.count(), 1)
        files = File.objects.last()
        self.assertEqual(files.created_by, user)
        self.assertEqual(files.modified_by, user)

    def test_redirects_to_file_list_on_success(self):
        """Should redirect to the file list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(),
            {"name": "616.mp3", "file": test_txt_file()},
        )

        self.assertRedirects(response, reverse("user_files:FileList"))

    def test_breadcrumbs_active(self):
        """
        FileCreate should have breadcrumbs for the following views:
        FileList
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                FileList.get_breadcrumb(),
            ],
        )


class FileUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.file = FileFactory()

    def get_url(self):
        return reverse("user_files:FileUpdate", args=[self.file.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """
        Should require permission to change user files.
        """
        self.assertPermissionRequired(
            self.get_url(),
            "user_files.change_file",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete user files.
        """
        self.client.force_login(self.file.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` and not `created_by` to the current user on update."""
        previous_created_by = self.file.created_by
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            {"name": "616.mp3", "file": test_txt_file()},
        )

        self.assertEqual(File.objects.count(), 1)
        file = File.objects.last()
        self.assertEqual(file.created_by, previous_created_by)
        self.assertEqual(file.modified_by, user)

    def test_redirects_to_file_list_on_success(self):
        """Should redirect to the file list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(),
            {"name": "616.mp3", "file": test_txt_file()},
        )

        self.assertRedirects(response, reverse("user_files:FileList"))

    def test_breadcrumbs_active(self):
        """
        FileUpdate should have breadcrumbs for the following views:
        FileList
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                FileList.get_breadcrumb(),
            ],
        )


class FileDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.file = FileFactory()

    def get_url(self):
        return reverse("user_files:FileDelete", args=[self.file.slug])

    def test_redirects_to_poll_list_on_success(self):
        """Should redirect to the file list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse("user_files:FileList"))

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """
        Should require permission to delete user files.
        """
        self.assertPermissionRequired(
            self.get_url(),
            "user_files.delete_file",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete user files.
        """
        self.client.force_login(self.file.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_breadcrumbs_active(self):
        """
        FileDelete should have breadcrumbs for the following views:
        FileList
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                FileList.get_breadcrumb(),
            ],
        )
