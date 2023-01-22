from django.conf import settings
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data

from .factories import (
    InstrumentFactory,
    InstrumentGroupFactory,
    InstrumentLocationFactory,
    InstrumentTypeDetectionExceptionFactory,
    InstrumentTypeDetectionKeywordFactory,
    InstrumentTypeFactory,
)
from .forms import InstrumentFormset, InstrumentGroupLeadersForm
from .models import (
    Instrument,
    InstrumentType,
    InstrumentTypeDetectionException,
    InstrumentTypeDetectionKeyword,
)


class InstrumentGroupTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_group = InstrumentGroupFactory(name="Tuba")

    def test_to_str(self):
        self.assertEqual(str(self.instrument_group), "Tuba")

    def test_name_unique(self):
        """`name` should be unique."""
        with self.assertRaises(IntegrityError):
            InstrumentGroupFactory(name=self.instrument_group.name)


class InstrumentTypeTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_type = InstrumentTypeFactory()

    def test_to_str(self):
        """`__str__` should be equal to the instrument type's name."""
        self.assertEqual(str(self.instrument_type), self.instrument_type.name)

    def test_name_unique(self):
        """`name` should be unique."""
        with self.assertRaises(IntegrityError):
            InstrumentTypeFactory(name=self.instrument_type.name)

    def test_unknown_creates_new_instrument_type_if_not_exist(self):
        """Should create a new instrument type if it doesn't already exist."""
        self.assertEqual(InstrumentType.objects.count(), 1)
        InstrumentType.unknown()
        self.assertEqual(InstrumentType.objects.count(), 2)

    def test_unknown_reuses_existing_instrument_type(self):
        """Should re-use existing instrument type if it exists."""
        unknown = InstrumentType.unknown()
        self.assertEqual(InstrumentType.objects.count(), 2)
        self.assertEqual(unknown, InstrumentType.unknown())
        self.assertEqual(InstrumentType.objects.count(), 2)

    def test_should_reuse_existing_instrument_type_even_if_different_group(self):
        """Should re-use the existing instrument type, even if it has a different group."""
        unknown = InstrumentType.unknown()
        self.assertEqual(InstrumentType.objects.count(), 2)
        unknown.instrument_group = InstrumentGroupFactory()
        self.assertEqual(unknown, InstrumentType.unknown())
        self.assertEqual(InstrumentType.objects.count(), 2)


class InstrumentTypeDetectionKeywordTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.detection_keyword = InstrumentTypeDetectionKeywordFactory()

    def test_to_str(self):
        """`__str__` should equal the keyword."""
        self.assertEqual(str(self.detection_keyword), self.detection_keyword.keyword)

    def test_keyword_unique(self):
        """Keywords should be unique."""
        with self.assertRaises(IntegrityError):
            InstrumentTypeDetectionKeywordFactory(
                keyword=self.detection_keyword.keyword
            )

    def test_ordering(self):
        """Should be ordered by the keyword."""
        self.assertModelOrdering(
            InstrumentTypeDetectionKeyword,
            InstrumentTypeDetectionKeywordFactory,
            [
                {"keyword": "a"},
                {"keyword": "b"},
                {"keyword": "c"},
            ],
        )


class InstrumentTypeDetectionExceptionTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.detection_exception = InstrumentTypeDetectionExceptionFactory()

    def test_to_str(self):
        """`__str__` should equal the exception."""
        self.assertEqual(
            str(self.detection_exception), self.detection_exception.exception
        )

    def test_exception_unique_for_each_instrument(self):
        """Exceptions should be unique for each instrument."""
        InstrumentTypeDetectionExceptionFactory(
            exception=self.detection_exception.exception,
            instrument_type=InstrumentTypeFactory(),
        )

        with self.assertRaises(IntegrityError):
            InstrumentTypeDetectionExceptionFactory(
                exception=self.detection_exception.exception,
                instrument_type=self.detection_exception.instrument_type,
            )

    def test_ordering(self):
        """Should be ordered by the exception."""
        self.assertModelOrdering(
            InstrumentTypeDetectionException,
            InstrumentTypeDetectionExceptionFactory,
            [
                {"exception": "a"},
                {"exception": "b"},
                {"exception": "c"},
            ],
        )


class InstrumentLocationTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_location = InstrumentLocationFactory(name="Lager")

    def test_to_str(self):
        self.assertEqual(str(self.instrument_location), "Lager")

    def test_name_unique(self):
        """`name` should be unique."""
        with self.assertRaises(IntegrityError):
            InstrumentLocationFactory(name=self.instrument_location.name)


class InstrumentTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument = InstrumentFactory()

    def test_to_str(self):
        """`__str__` should include instrument type and identifier."""
        self.assertEqual(
            str(self.instrument), f"{self.instrument.type} {self.instrument.identifier}"
        )

    def test_type_and_identifier_unique_togther(self):
        """Should enforce uniqueness of `type` and `identifier`."""
        with self.assertRaises(IntegrityError):
            InstrumentFactory(
                type=self.instrument.type, identifier=self.instrument.identifier
            )


class InstrumentListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentList")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())


class InstrumentsUpdateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentsUpdate")

    def create_post_data(self, num_of_new=0):
        return create_formset_post_data(
            InstrumentFormset,
            data=self.formset_data,
            total_forms=1 + num_of_new,
            initial_forms=1,
        )

    def setUp(self):
        self.instrument = InstrumentFactory(
            type=InstrumentTypeFactory(name="Bassklarinett")
        )
        self.formset_data = [
            {
                "type": self.instrument.type.pk,
                "identifier": self.instrument.identifier,
                "user": "",
                "location": self.instrument.location.pk,
                "serial_number": self.instrument.serial_number,
                "comment": self.instrument.comment,
                "state": self.instrument.state,
                "id": self.instrument.pk,
            }
        ]

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "instruments.add_instrument",
            "instruments.change_instrument",
            "instruments.delete_instrument",
        )

    def test_create_instrument(self):
        type = InstrumentTypeFactory()
        location = InstrumentLocationFactory()
        self.formset_data.append(
            {
                "type": type.pk,
                "identifier": "14",
                "location": location.pk,
                "state": Instrument.State.GOOD,
            }
        )
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data(num_of_new=1))
        self.assertEqual(Instrument.objects.count(), 2)

    def test_update_instrument(self):
        user = UserFactory()
        self.formset_data[0]["identifier"] = "plast, gul"
        self.formset_data[0]["user"] = user.pk
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data())
        self.instrument.refresh_from_db()
        self.assertEqual(self.instrument.identifier, "plast, gul")
        self.assertEqual(self.instrument.user, user)

    def test_delete_instrument(self):
        self.formset_data[0]["DELETE"] = "on"
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(Instrument.objects.count(), 0)


class InstrumentGroupLeaderListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentGroupLeaderList")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())


class InstrumentGroupLeadersFormTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentGroupLeadersUpdate")

    def setUp(self):
        self.user = UserFactory()
        self.instrument_leader_group = Group.objects.create(
            name=settings.INSTRUMENT_GROUP_LEADERS_NAME
        )
        self.instrument_leader_group.user_set.add(self.user)

    def test_initial(self):
        """Initial data should equal instrument group leaders."""
        form = InstrumentGroupLeadersForm()
        self.assertQuerysetEqual(form["instrument_group_leaders"].initial, [self.user])


class InstrumentGroupLeadersUpdateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("instruments:InstrumentGroupLeadersUpdate")

    def setUp(self):
        self.instrument_leader_group = Group.objects.create(
            name=settings.INSTRUMENT_GROUP_LEADERS_NAME
        )

        self.form = InstrumentGroupLeadersForm()

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "accounts.edit_instrument_group_leaders",
        )

    def test_adds_new_removes_existing_instrument_group_leaders(self):
        """Should remove existing instrument group leaders."""
        user = UserFactory()
        self.instrument_leader_group.user_set.add(user)

        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url())
        self.assertQuerysetEqual(self.instrument_leader_group.user_set.all(), [])

    def test_adds_specified_instrument_group_leaders(self):
        """Should add specified instrument group leaders."""
        user = UserFactory()

        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), {"instrument_group_leaders": [user.pk]})
        self.assertQuerysetEqual(self.instrument_leader_group.user_set.all(), [user])
