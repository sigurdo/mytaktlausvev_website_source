import shutil
import tempfile
from http import HTTPStatus

from django.forms import FileField, ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.views.generic import View

from accounts.factories import UserFactory

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestMixin(TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        return super().tearDownClass()

    def assertLoginRequired(self, url):
        """
        Asserts that `url` requires login by checking for a redirect to the `login` view.
        Logs out before checking.
        """
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def assertPermissionRequired(
        self,
        url,
        *permissions,
        method="get",
        status_success=HTTPStatus.OK,
        status_no_permission=HTTPStatus.FORBIDDEN,
    ):
        """Asserts that `url` requires `permission`."""
        self.client.force_login(UserFactory())
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, status_no_permission)

        self.client.force_login(UserFactory(permissions=permissions))
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, status_success)


class CleanAllFilesMixin:
    """
    Mixin that ensures that all files uploaded
    to a `FileField` are cleaned.

    For some reason, Django only calls field.clean() on the last file, so
    we have to call field.clean() on all others manually.
    """

    def _clean_fields(self):
        super()._clean_fields()
        for name, field in self.fields.items():
            if isinstance(field, FileField):
                for file in self.files.getlist(name)[:-1]:
                    try:
                        field.clean(file)
                    except ValidationError as exception:
                        self.add_error(name, exception)


class BreadcrumbsMixin(View):
    def get_breadcrumbs(self) -> list:
        """
        Should be overrided and return a list of breadcrumb dicts on the following format:
        [
            {
                "url": "<URL the breadcrumb should redirect to>",
                "name": "<name or label for the breadcrumb>",
            },
            ...
        ]
        """
        raise NotImplementedError(
            "BreadcrumbsMixin.get_breadcrumbs() must be overridden"
        )

    def get_context_data(self, **kwargs):
        kwargs["breadcrumbs"] = self.get_breadcrumbs()
        return super().get_context_data(**kwargs)
