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

    def test_breadcrumbs(self):
        """
        ActiveRepertoires should have an empty list of breadcrumbs
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(breadcrumbs, [])


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

    def test_breadcrumbs_active(self):
        """
        RepertoireDetail for an active repertoire should have breadcrumbs for the following views:
        ActiveRepertoires
        """
        repertoire = RepertoireFactory(active_until=None)
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
            ],
        )

    def test_breadcrumbs_old(self):
        """
        RepertoireDetail for an old repertoire should have breadcrumbs for the following views:
        ActiveRepertoires / OldRepertoires
        """
        repertoire = RepertoireFactory(active_until=now() - timedelta(days=1))
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
                OldRepertoires.get_breadcrumb(),
            ],
        )


class OldRepertoiresTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("repertoire:OldRepertoires")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_breadcrumbs(self):
        """
        OldRepertoires should have breadcrumbs for the following views:
        ActiveRepertoires
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
            ],
        )


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

    def test_breadcrumbs(self):
        """
        RepertoireCreate should have breadcrumbs for the following views:
        ActiveRepertoires
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
            ],
        )


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

    def test_breadcrumbs_active(self):
        """
        RepertoireUpdate for an active repertoire should have breadcrumbs for the following views:
        ActiveRepertoires / RepertoireDetail
        """
        repertoire = RepertoireFactory(active_until=None)
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
                RepertoireDetail.get_breadcrumb(repertoire),
            ],
        )

    def test_breadcrumbs_old(self):
        """
        RepertoireUpdate for an old repertoire should have breadcrumbs for the following views:
        ActiveRepertoires / OldRepertoires / RepertoireDetail
        """
        repertoire = RepertoireFactory(active_until=now() - timedelta(days=1))
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
                OldRepertoires.get_breadcrumb(),
                RepertoireDetail.get_breadcrumb(repertoire),
            ],
        )


class RepertoireDeleteTestSuite(TestMixin, TestCase):
    def get_url(self, repertoire=None):
        repertoire = repertoire or self.repertoire
        return reverse("repertoire:RepertoireDelete", args=[repertoire.slug])

    def setUp(self):
        self.repertoire = RepertoireFactory()

    def test_requires_permission(self):
        self.assertPermissionRequired(self.get_url(), "repertoire.delete_repertoire")

    def test_breadcrumbs_active(self):
        """
        RepertoireDelete for an active repertoire should have breadcrumbs for the following views:
        ActiveRepertoires / RepertoireDetail
        """
        repertoire = RepertoireFactory(active_until=None)
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
                RepertoireDetail.get_breadcrumb(repertoire),
            ],
        )

    def test_breadcrumbs_old(self):
        """
        RepertoireDelete for an old repertoire should have breadcrumbs for the following views:
        ActiveRepertoires / OldRepertoires / RepertoireDetail
        """
        repertoire = RepertoireFactory(active_until=now() - timedelta(days=1))
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
                OldRepertoires.get_breadcrumb(),
                RepertoireDetail.get_breadcrumb(repertoire),
            ],
        )


class RepertoirePdfTestSuite(TestMixin, TestCase):
    def get_url(self, repertoire=None):
        repertoire = repertoire or self.repertoire
        return reverse("repertoire:RepertoirePdf", args=[repertoire.slug])

    def create_post_data(self, data=None):
        if data is None:
            data = [
                {
                    "part": self.score_1.find_user_part(self.user).pk,
                    "amount": self.amount_1,
                },
                {
                    "part": self.score_2.find_user_part(self.user).pk,
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
        (self.score_1, self.score_2) = (ScoreFactory(), ScoreFactory())
        (self.amount_1, self.amount_2) = (1, 2)
        self.repertoire = RepertoireFactory(scores=[self.score_1, self.score_2])
        (self.favorite_1, self.favorite_2) = (
            FavoritePartFactory(part__pdf__score=self.score_1, user=self.user),
            FavoritePartFactory(part__pdf__score=self.score_2, user=self.user),
        )

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(), self.create_post_data())
        self.assertEqual(response["content-type"], "application/pdf")
        pdf_reader = PdfReader(BytesIO(response.getvalue()))
        self.assertEqual(len(pdf_reader.pages), 3)

    # The "z" in the name is there because this test case has to be run after `test_post`, else `test_post` will fail.
    # I have no idea why.
    def test_z_breadcrumbs_active(self):
        """
        RepertoirePdf for an active repertoire should have breadcrumbs for the following views:
        ActiveRepertoires / RepertoireDetail
        """
        repertoire = RepertoireFactory(active_until=None)
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
                RepertoireDetail.get_breadcrumb(repertoire),
            ],
        )

    # The "z" in the name is there because this test case has to be run after `test_post`, else `test_post` will fail.
    # I have no idea why.
    def test_z_breadcrumbs_old(self):
        """
        RepertoirePdf for an old repertoire should have breadcrumbs for the following views:
        ActiveRepertoires / OldRepertoires / RepertoireDetail
        """
        repertoire = RepertoireFactory(active_until=now() - timedelta(days=1))
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url(repertoire)).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ActiveRepertoires.get_breadcrumb(),
                OldRepertoires.get_breadcrumb(),
                RepertoireDetail.get_breadcrumb(repertoire),
            ],
        )
