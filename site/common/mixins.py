import shutil
import tempfile
from http import HTTPStatus
from random import shuffle

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.test import TestCase, override_settings
from django.urls import reverse

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

    def assertModelOrdering(self, model, factory, factory_kwargs, number_of_tests=None):
        """
        Asserts that `model` instances generated with `factory` and `factory_kwargs` are ordered
        in the same order `factory_kwargs` are provided. `factory_kwargs` is an iterable of
        dictionaries with kwargs for `factory`. Requires that the length of `factory_kwargs` is
        minimum 2, unless there is no way in which the test can fail.

        Uses shuffling and enumerations to ensure that the ordering of the factory
        calls is not what produces the correct ordering in the end.

        If `number_of_tests` is not given it will produce the following tests based on the
        number of specified instances:

        - 2: 9
        - 3: 5
        - 4: 3
        - 5: 2
        - any higher: 1

        This gives certainity that it was not correct by luck also for low numbers of instances.
        """
        factory_kwargs_enumerated = list(enumerate(factory_kwargs))
        if len(factory_kwargs_enumerated) < 2:
            raise Exception(
                f"Must have minimum 2 instances to verify ordering, but got only {len(factory_kwargs)}"
            )
        if number_of_tests is None:
            number_of_tests = 8 // 2 ** (len(factory_kwargs_enumerated) - 2) + 1
        for i in range(number_of_tests):
            shuffle(factory_kwargs_enumerated)
            model.objects.all().delete()
            entries_enumerated = [
                (i, factory(**kwargs)) for i, kwargs in factory_kwargs_enumerated
            ]
            entries_enumerated.sort(key=lambda element: element[0])
            for i, entry in enumerate(model.objects.all()):
                self.assertEqual(entry, entries_enumerated[i][1])


class PermissionOrCreatedMixin(PermissionRequiredMixin):
    """
    Mixin that permits the user if the user has the correct permissions,
    or if the user created the view's object.
    Designed to be used with SingleObjectMixin.

    Permission functionality is equivalent to `PermissionRequiredMixin`.

    `field_created_by` specifies which field to get the object's author from.
    Defaults to `CreatedModifiedMixin`'s `created_by`.

    `user_has_created` checks if the user created the object.
    """

    field_created_by = "created_by"

    def get_permission_check_object(self):
        return self.get_object()

    def user_has_created(self):
        """Returns `True` if the user created `object`, `False` otherwise."""
        created_by = getattr(
            self.get_permission_check_object(), self.field_created_by, None
        )
        return created_by == self.request.user

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.user_has_created() or self.has_permission()
        if not has_permission:
            return self.handle_no_permission()
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
