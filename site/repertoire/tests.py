from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from PyPDF2 import PdfFileReader

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data
from sheetmusic.factories import FavoritePartFactory

from .factories import RepertoireEntryFactory, RepertoireFactory
from .forms import RepertoireEntryFormset, RepertoirePdfFormset


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


class RepertoireEntryTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.entry = RepertoireEntryFactory(
            repertoire__name="Vårkonsert", score__title="Ice Cream"
        )

    def test_to_str(self):
        self.assertEqual(str(self.entry), "Vårkonsert - Ice Cream")


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
        self.assertRedirects(response, reverse("repertoire:RepertoireList"))


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
        self.assertRedirects(response, reverse("repertoire:RepertoireList"))


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
