from datetime import datetime, timedelta
from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware
from PyPDF2 import PdfFileReader

from accounts.factories import SuperUserFactory, UserFactory
from common.breadcrumbs.breadcrumbs import Breadcrumb
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data
from sheetmusic.factories import FavoritePartFactory

from .factories import RepertoireEntryFactory, RepertoireFactory
from .forms import RepertoireEntryFormset, RepertoirePdfFormset
from .models import Repertoire
from .views import repertoire_breadcrumbs


class RepertoireManagerTestSuite(TestMixin, TestCase):
    def test_active_includes_active(self):
        repertoire = RepertoireFactory(
            always_active=True,
        )
        result = Repertoire.objects.active()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], repertoire)

    def test_active_includes_future_inactive(self):
        repertoire = RepertoireFactory(
            always_active=False,
            active_until=make_aware(datetime.now() + timedelta(days=14)).date(),
        )
        result = Repertoire.objects.active()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], repertoire)

    def test_active_does_not_include_inactive(self):
        RepertoireFactory(
            always_active=False,
        )
        result = Repertoire.objects.active()
        self.assertEqual(len(result), 0)

    def test_active_does_not_include_old_inactive(self):
        RepertoireFactory(
            always_active=False,
            active_until=make_aware(datetime.now() - timedelta(days=14)).date(),
        )
        result = Repertoire.objects.active()
        self.assertEqual(len(result), 0)


class RepertoireTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.repertoire = RepertoireFactory(name="Marsjhefte")
        self.entry = RepertoireEntryFactory(repertoire=self.repertoire)
        self.favorite = FavoritePartFactory(
            part__pdf__score=self.entry.score, user=self.user
        )

    def test_to_str(self):
        self.assertEqual(str(self.repertoire), "Marsjhefte")

    def test_pdf_file(self):
        pdf_file = self.repertoire.favorite_parts_pdf_file(self.user)
        self.assertEqual(type(pdf_file), BytesIO)

    def test_pdf_filename(self):
        pdf_filename = self.repertoire.favorite_parts_pdf_filename(self.user)
        self.assertEqual(pdf_filename, f"marsjhefte-{self.user.slug}.pdf")

    def test_pdf_file_no_favorite(self):
        self.favorite.delete()
        self.assertRaises(Exception, self.repertoire.favorite_parts_pdf_file, self.user)

    def test_is_active_includes_active(self):
        repertoire = RepertoireFactory(
            always_active=True,
        )
        self.assertTrue(repertoire.is_active())

    def test_is_active_includes_future_inactive(self):
        repertoire = RepertoireFactory(
            always_active=False,
            active_until=make_aware(datetime.now() + timedelta(days=14)).date(),
        )
        self.assertTrue(repertoire.is_active())

    def test_is_active_does_not_include_inactive(self):
        repertoire = RepertoireFactory(
            always_active=False,
        )
        self.assertFalse(repertoire.is_active())

    def test_is_active_does_not_include_old_inactive(self):
        repertoire = RepertoireFactory(
            always_active=False,
            active_until=make_aware(datetime.now() - timedelta(days=14)).date(),
        )
        self.assertFalse(repertoire.is_active())

    def test_get_absolute_url(self):
        self.assertEqual(
            self.repertoire.get_absolute_url(),
            reverse("repertoire:RepertoireDetail", args=[self.repertoire.slug]),
        )


class RepertoireEntryTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.entry = RepertoireEntryFactory(
            repertoire__name="Vårkonsert", score__title="Ice Cream"
        )

    def test_to_str(self):
        self.assertEqual(str(self.entry), "Vårkonsert - Ice Cream")


class RepertoireBreadcrumbsTestSuite(TestMixin, TestCase):
    def test_base(self):
        breadcrumbs = repertoire_breadcrumbs()
        self.assertEqual(
            breadcrumbs,
            [
                Breadcrumb(
                    reverse("repertoire:RepertoireList"),
                    "Alle repertoar",
                )
            ],
        )

    def test_current(self):
        breadcrumbs = repertoire_breadcrumbs(current=True)
        self.assertEqual(
            breadcrumbs[1],
            Breadcrumb(
                reverse("repertoire:ActiveRepertoires"),
                "Aktive",
            ),
        )

    def test_repertoire(self):
        repertoire = RepertoireFactory()
        breadcrumbs = repertoire_breadcrumbs(repertoire=repertoire)
        self.assertEqual(
            breadcrumbs[1],
            Breadcrumb(
                reverse("repertoire:RepertoireDetail", args=[repertoire.slug]),
                str(repertoire),
            ),
        )


class ActiveRepertoiresTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        self.assertLoginRequired(reverse("repertoire:ActiveRepertoires"))

    def test_get_queryset(self):
        RepertoireFactory(always_active=True)
        self.client.force_login(UserFactory())
        response = self.client.get(reverse("repertoire:ActiveRepertoires"))
        self.assertEqual(
            list(response.context["repertoires"]), list(Repertoire.objects.active())
        )


class RepertoireDetailTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.repertoire = RepertoireFactory(always_active=True)

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse("repertoire:RepertoireDetail", args=[self.repertoire.slug])
        )

    def test_context_object_name(self):
        self.client.force_login(UserFactory())
        response = self.client.get(
            reverse("repertoire:RepertoireDetail", args=[self.repertoire.slug])
        )
        self.assertEqual(response.context["repertoire"], self.repertoire)


class RepertoireListTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        self.assertLoginRequired(reverse("repertoire:RepertoireList"))


class RepertoireCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.test_data = {
            "name": "Repertoire",
            "order": 0,
            **create_formset_post_data(
                RepertoireEntryFormset,
                total_forms=0,
                initial_forms=0,
            ),
        }

    def test_requires_login(self):
        self.assertLoginRequired(reverse("repertoire:RepertoireCreate"))

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("repertoire:RepertoireCreate"),
            "repertoire.add_repertoire",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            reverse("repertoire:RepertoireCreate"), self.test_data
        )
        self.assertRedirects(response, reverse("repertoire:ActiveRepertoires"))


class RepertoireUpdateTestSuite(TestMixin, TestCase):
    def create_post_data(self, data=[]):
        return create_formset_post_data(
            RepertoireEntryFormset,
            data=data,
        )

    def get_url(self):
        return reverse("repertoire:RepertoireUpdate", args=[self.repertoire.slug])

    def setUp(self):
        self.repertoire = RepertoireFactory()
        self.entry = RepertoireEntryFactory(repertoire=self.repertoire)
        self.test_data = self.create_post_data(
            data=[{"score": self.entry.score.pk, "id": self.entry.pk}]
        )
        self.test_data["name"] = self.repertoire.name
        self.test_data["order"] = self.repertoire.order

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "repertoire.change_repertoire",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.test_data)
        self.assertRedirects(response, reverse("repertoire:ActiveRepertoires"))


class RepertoireDeleteTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("repertoire:RepertoireDelete", args=[self.repertoire.slug])

    def setUp(self):
        self.repertoire = RepertoireFactory()

    def test_requires_permission(self):
        self.assertPermissionRequired(self.get_url(), "repertoire.delete_repertoire")


class RepertoirePdfTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("repertoire:RepertoirePdf", args=[self.entry.repertoire.slug])

    def create_post_data(self, data=None):
        if data is None:
            data = [
                {
                    "part": self.entry.score.find_user_part(self.user).pk,
                    "amount": self.amount,
                },
                {
                    "part": self.entry_2.score.find_user_part(self.user).pk,
                    "amount": self.amount_2,
                },
            ]
        return create_formset_post_data(
            RepertoirePdfFormset,
            total_forms=2,
            initial_forms=2,
            data=data,
        )

    def setUp(self):
        self.user = UserFactory()
        self.entry = RepertoireEntryFactory()
        self.amount = 1
        self.entry_2 = RepertoireEntryFactory(repertoire=self.entry.repertoire)
        self.amount_2 = 2
        self.favorite = FavoritePartFactory(
            part__pdf__score=self.entry.score, user=self.user
        )
        self.favorite_2 = FavoritePartFactory(
            part__pdf__score=self.entry_2.score, user=self.user
        )

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(response["content-type"], "application/pdf")
        pdf_reader = PdfFileReader(BytesIO(response.getvalue()))
        self.assertEqual(pdf_reader.getNumPages(), 3)
