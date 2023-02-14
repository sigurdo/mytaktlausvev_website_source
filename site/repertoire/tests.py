from datetime import timedelta
from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from pypdf import PdfReader

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data
from sheetmusic.factories import FavoritePartFactory, ScoreFactory

from .factories import RepertoireFactory
from .forms import RepertoirePdfFormset
from .models import Repertoire
from .views import ActiveRepertoires, OldRepertoires, RepertoireDetail


class RepertoireManagerTestSuite(TestMixin, TestCase):
    def test_active_includes_active_until_none(self):
        repertoire = RepertoireFactory(active_until=None)
        result = Repertoire.objects.active()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], repertoire)

    def test_active_includes_active_until_future(self):
        repertoire = RepertoireFactory(active_until=(now() + timedelta(days=14)).date())
        result = Repertoire.objects.active()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], repertoire)

    def test_active_does_not_include_active_until_past(self):
        RepertoireFactory(active_until=(now() - timedelta(days=14)).date())
        result = Repertoire.objects.active()
        self.assertEqual(len(result), 0)

    def test_active_on_date_does_not_include_future_created(self):
        RepertoireFactory()
        result = Repertoire.objects.active(date=(now() - timedelta(days=1)).date())
        self.assertEqual(len(result), 0)

    def test_active_on_date_does_not_include_past_active(self):
        RepertoireFactory(active_until=(now() - timedelta(days=1)).date())
        result = Repertoire.objects.active(date=now().date())
        self.assertEqual(len(result), 0)


class RepertoireTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory(name="Leiar")
        self.score = ScoreFactory()
        self.repertoire = RepertoireFactory(name="Marsjhefte", scores=[self.score])
        self.favorite = FavoritePartFactory(part__pdf__score=self.score, user=self.user)

    def test_to_str(self):
        self.assertEqual(str(self.repertoire), "Marsjhefte")

    def test_pdf_file(self):
        pdf_file = self.repertoire.favorite_parts_pdf_file(self.user)
        self.assertEqual(type(pdf_file), BytesIO)

    def test_pdf_filename(self):
        pdf_filename = self.repertoire.favorite_parts_pdf_filename(self.user)
        self.assertEqual(pdf_filename, "Marsjhefte_Leiar.pdf")

    def test_pdf_file_no_favorite(self):
        self.favorite.delete()
        self.assertRaises(Exception, self.repertoire.favorite_parts_pdf_file, self.user)

    def test_is_active_includes_active_until_none(self):
        repertoire = RepertoireFactory(
            active_until=None,
        )
        self.assertTrue(repertoire.is_active())

    def test_is_active_includes_active_until_future(self):
        repertoire = RepertoireFactory(
            active_until=(now() + timedelta(days=14)).date(),
        )
        self.assertTrue(repertoire.is_active())

    def test_is_active_does_not_include_active_until_past(self):
        repertoire = RepertoireFactory(
            active_until=(now() - timedelta(days=14)).date(),
        )
        self.assertFalse(repertoire.is_active())

    def test_get_absolute_url(self):
        self.assertEqual(
            self.repertoire.get_absolute_url(),
            reverse("repertoire:RepertoireDetail", args=[self.repertoire.slug]),
        )

    def test_slug_unique(self):
        other = RepertoireFactory(slug=self.repertoire.slug)
        self.assertNotEqual(self.repertoire.slug, other.slug)


class ActiveRepertoiresTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("repertoire:ActiveRepertoires")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_get_queryset(self):
        RepertoireFactory()
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(
            list(response.context["repertoires"]), list(Repertoire.objects.active())
        )


class RepertoireDetailTestSuite(TestMixin, TestCase):
    def get_url(self, repertoire=None):
        repertoire = repertoire or self.repertoire
        return reverse("repertoire:RepertoireDetail", args=[repertoire.slug])

    def setUp(self):
        self.repertoire = RepertoireFactory()

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_context_object_name(self):
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.context["repertoire"], self.repertoire)


class OldRepertoiresTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("repertoire:OldRepertoires")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())


class RepertoireCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("repertoire:RepertoireCreate")

    def setUp(self):
        self.score = ScoreFactory()
        self.test_data = {
            "name": "Repertoire",
            "order": 0,
            "scores": [self.score.pk],
        }

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(self.get_url(), "repertoire.add_repertoire")

    def test_success_redirect(self):
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url(), self.test_data)
        self.assertRedirects(response, reverse("repertoire:ActiveRepertoires"))


class RepertoireUpdateTestSuite(TestMixin, TestCase):
    def get_url(self, repertoire=None):
        repertoire = repertoire or self.repertoire
        return reverse("repertoire:RepertoireUpdate", args=[repertoire.slug])

    def setUp(self):
        self.score = ScoreFactory()
        self.repertoire = RepertoireFactory(scores=[self.score])
        self.test_data = {
            "name": self.repertoire.name,
            "order": self.repertoire.order,
            "scores": [self.score.pk],
        }

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
    def get_url(self, repertoire=None):
        repertoire = repertoire or self.repertoire
        return reverse("repertoire:RepertoireDelete", args=[repertoire.slug])

    def setUp(self):
        self.repertoire = RepertoireFactory()

    def test_requires_permission(self):
        self.assertPermissionRequired(self.get_url(), "repertoire.delete_repertoire")


class RepertoirePdfTestSuite(TestMixin, TestCase):
    def get_url(self, repertoire=None):
        repertoire = repertoire or self.repertoire
        return reverse("repertoire:RepertoirePdf", args=[repertoire.slug])

    def create_post_data(self, data=None):
        if data is None:
            data = [
                {
                    "part": self.scores[i].find_user_part(self.user).pk,
                    "amount": self.amounts[i],
                }
                for i in range(2)
            ]
        return create_formset_post_data(
            RepertoirePdfFormset,
            total_forms=2,
            initial_forms=2,
            data=data,
        )

    def setUp(self):
        self.user = UserFactory()
        # Titles are required to ensure consistent ordering on backend and in `create_post_data()`.
        self.scores = [ScoreFactory(title="A"), ScoreFactory(title="B")]
        self.amounts = [1, 2]
        self.repertoire = RepertoireFactory(scores=self.scores)
        self.favorites = [
            FavoritePartFactory(part__pdf__score=score, user=self.user)
            for score in self.scores
        ]

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(response["content-type"], "application/pdf")
        pdf_reader = PdfReader(BytesIO(response.getvalue()))
        self.assertEqual(len(pdf_reader.pages), 3)
