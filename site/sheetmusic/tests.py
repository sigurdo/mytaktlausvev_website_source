import os
from http import HTTPStatus

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from PyPDF2 import PdfFileReader

from accounts.factories import SuperUserFactory, UserFactory
from common.breadcrumbs.breadcrumbs import Breadcrumb
from common.mixins import TestMixin
from common.test_utils import (
    create_formset_post_data,
    test_image,
    test_pdf,
    test_pdf_multipage,
    test_txt_file,
)
from instruments.factories import InstrumentTypeFactory

from .factories import (
    EditFileFactory,
    FavoritePartFactory,
    PartFactory,
    PdfFactory,
    ScoreFactory,
)
from .forms import (
    EditEditFileFormset,
    EditPdfFormset,
    PartsUpdateAllFormset,
    PartsUpdateFormset,
)
from .models import EditFile, Part, Pdf, Score
from .views import nav_tabs_score_edit, sheetmusic_breadcrumbs


class ScoreManagerTestSuite(TestMixin, TestCase):
    def test_has_favorite_parts(self):
        """
        Should set `user_has_favorite_parts` depending on whether
        `user` has favorite parts for a score.
        """
        user = UserFactory()
        favorited_part = FavoritePartFactory(user=user).part
        not_favorited_part = PartFactory()

        scores = Score.objects.annotate_user_has_favorite_parts(user)
        self.assertTrue(
            scores.get(pk=favorited_part.pdf.score.pk).user_has_favorite_parts
        )
        self.assertFalse(
            scores.get(pk=not_favorited_part.pdf.score.pk).user_has_favorite_parts
        )


class ScoreTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_type = InstrumentTypeFactory()
        self.instrument_group = self.instrument_type.group
        self.score = ScoreFactory(title="Chirp")
        self.pdf_1 = PdfFactory(score=self.score)
        self.pdf_2 = PdfFactory(score=self.score)
        self.part_1 = PartFactory(pdf=self.pdf_1)
        self.part_2 = PartFactory(pdf=self.pdf_1)
        self.part_3 = PartFactory(pdf=self.pdf_2)
        self.part_4 = PartFactory(pdf=self.pdf_2)
        self.part_instrument_type = PartFactory(
            pdf=self.pdf_1, instrument_type=self.instrument_type
        )
        self.part_instrument_group = PartFactory(
            pdf=self.pdf_1,
            instrument_type=InstrumentTypeFactory(group=self.instrument_group),
        )
        FavoritePartFactory(part=self.part_1)
        FavoritePartFactory(part=self.part_2)
        FavoritePartFactory(part=self.part_3)
        FavoritePartFactory(part=self.part_4)
        FavoritePartFactory(part=self.part_instrument_type)
        FavoritePartFactory(part=self.part_instrument_group)

    def test_to_str(self):
        self.assertEqual(str(self.score), "Chirp")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.score.get_absolute_url(),
            reverse("sheetmusic:ScoreView", kwargs={"slug": self.score.slug}),
        )

    def test_find_user_part_favorite(self):
        """
        Checks that favorite part is found before instrument type part.
        """
        user = UserFactory(instrument_type=self.instrument_type)
        favorite_part = FavoritePartFactory(user=user, part__pdf=self.pdf_1)
        found_part = self.score.find_user_part(user)
        self.assertEqual(found_part, favorite_part.part)

    def test_find_user_part_type(self):
        """
        Checks that instrument type part is found before instrument group part.
        """
        user = UserFactory(instrument_type=self.instrument_type)
        found_part = self.score.find_user_part(user)
        self.assertEqual(found_part, self.part_instrument_type)

    def test_find_user_part_group(self):
        """
        Checks that instrument group part is found when neither favorite nor instrument type part exist.
        """
        user = UserFactory(
            instrument_type=InstrumentTypeFactory(group=self.instrument_group)
        )
        self.part_instrument_type.delete()
        found_part = self.score.find_user_part(user)
        self.assertEqual(found_part, self.part_instrument_group)

    def test_favorite_parts_pdf_file(self):
        """
        Checks that favorite_parts_pdf_file has 3 pages when user has 3 favorite parts.
        """
        user = UserFactory()
        for _ in range(3):
            part = PartFactory(pdf=self.pdf_1)
            FavoritePartFactory(user=user, part=part)
        pdf_stream = self.score.favorite_parts_pdf_file(user)
        pdf_reader = PdfFileReader(pdf_stream)
        self.assertEqual(pdf_reader.getNumPages(), 3)

    def test_favorite_parts_pdf_filename(self):
        """
        Checks that favorite_parts_pdf_filename returns "chirp-kultype.pdf" for a user named kultype.
        """
        user = UserFactory(username="kultype")
        result = self.score.favorite_parts_pdf_filename(user)
        self.assertEquals(result, "chirp-kultype.pdf")

    def test_is_processing(self):
        """
        Checks that `is_processing` returns True if any of its pdfs are being processed.
        """
        score = PdfFactory(processing=False).score
        PdfFactory(score=score, processing=True)
        self.assertTrue(score.is_processing())

    def test_is_not_processing(self):
        """
        Checks that `is_processing` returns False if none of its pdfs are being processed.
        """
        score = PdfFactory(processing=False).score
        self.assertFalse(score.is_processing())


class PdfTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.pdf = PdfFactory(filename_original="Chirp - saksofon.pdf")

    def test_slug_derived_from_original_filename_no_extension(self):
        """Should derive slug from original filename, without extension."""
        self.assertEqual(self.pdf.slug, slugify(self.pdf.filename_no_extension()))

    def test_to_str(self):
        """`__str__` should be the original filename."""
        self.assertEqual(str(self.pdf), self.pdf.filename_original)

    def test_filename_no_extension(self):
        """Should return the original filename, without an extension."""
        self.assertEqual(
            self.pdf.filename_no_extension(),
            os.path.splitext(self.pdf.filename_original)[0],
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.pdf.get_absolute_url(),
            reverse("sheetmusic:ScoreView", kwargs={"slug": self.pdf.score.slug}),
        )

    def test_num_of_pages(self):
        """
        Checks that there is 1 page in the default PDF.
        """
        self.assertEqual(self.pdf.num_of_pages(), 1)

    def test_find_parts_with_sheatless(self):
        """
        Checks that sheatless understands that there is written tuba inside the PDF.
        """
        InstrumentTypeFactory(name="Fløyte", detection_keywords=["Fløyte"])
        InstrumentTypeFactory(name="Klarinett", detection_keywords=["Klarinett"])
        tuba = InstrumentTypeFactory(name="Tuba", detection_keywords=["Tuba"])
        self.pdf.find_parts_with_sheatless()
        self.pdf.refresh_from_db()
        self.assertEqual(self.pdf.parts.count(), 1)
        self.assertEqual(self.pdf.parts.first().instrument_type, tuba)

    def test_find_parts_from_original_filename(self):
        """
        Checks that find_parts_from_original_filename understands that the original filename indicates saxophone.
        """
        InstrumentTypeFactory(name="Fløyte", detection_keywords=["Fløyte"])
        InstrumentTypeFactory(name="Klarinett", detection_keywords=["Klarinett"])
        saxophone = InstrumentTypeFactory(
            name="Altsaksofon", detection_keywords=["Saksofon"]
        )
        self.pdf.find_parts_from_original_filename()
        self.pdf.refresh_from_db()
        self.assertEqual(self.pdf.parts.count(), 1)
        self.assertEqual(self.pdf.parts.first().instrument_type, saxophone)

    def test_create_part_auto_number(self):
        """
        Checks that create_part_auto_number first creates a part with no part_number and then updates
        the old part_number to 1 on the second call with the same instrument type.
        """
        flute = InstrumentTypeFactory(name="Fløyte")
        self.pdf.create_part_auto_number(instrument_type=flute, from_page=1, to_page=1)
        self.pdf.refresh_from_db()
        self.assertEqual(self.pdf.parts.count(), 1)
        self.assertEqual(self.pdf.parts.first().instrument_type, flute)
        self.assertEqual(self.pdf.parts.first().part_number, None)
        self.pdf.create_part_auto_number(instrument_type=flute, from_page=1, to_page=1)
        self.pdf.refresh_from_db()
        self.assertEqual(self.pdf.parts.count(), 2)
        self.assertEqual(self.pdf.parts.first().part_number, 1)
        self.assertEqual(self.pdf.parts.last().part_number, 2)


class PartTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.instrument_type = InstrumentTypeFactory(name="Klarinett")
        self.part = PartFactory(
            instrument_type=self.instrument_type, part_number=1, note="i Eb"
        )
        self.pdf = self.part.pdf

    def test_to_str(self):
        """
        Checks that __str__ returns "Klarinett 1 (i Eb)"
        """
        self.assertEqual(str(self.part), "Klarinett 1 (i Eb)")

    def test_unique(self):
        """
        Checks that you cannot create parts that have the same instrument_type, part_number, note and pdf.
        """
        PartFactory(part_number=1, note="i Eb", pdf=self.pdf)
        PartFactory(instrument_type=self.instrument_type, note="i Eb", pdf=self.pdf)
        PartFactory(instrument_type=self.instrument_type, part_number=1, pdf=self.pdf)
        PartFactory(instrument_type=self.instrument_type, part_number=1, note="i Eb")
        with self.assertRaises(IntegrityError):
            PartFactory(
                instrument_type=self.instrument_type,
                part_number=1,
                note="i Eb",
                pdf=self.pdf,
            )

    def test_ordering(self):
        """
        Checks that default ordering of parts is like this:
        1. Klarinett
        2. Klarinett 1 (i Eb)
        3. Klarinett 2
        4. Klarinett 2 (i Eb)
        """
        self.part.delete()
        self.assertModelOrdering(
            Part,
            PartFactory,
            [
                {
                    "instrument_type": self.instrument_type,
                    "part_number": None,
                    "pdf": self.pdf,
                },
                {
                    "instrument_type": self.instrument_type,
                    "part_number": 1,
                    "note": "i Eb",
                    "pdf": self.pdf,
                },
                {
                    "instrument_type": self.instrument_type,
                    "part_number": 2,
                    "pdf": self.pdf,
                },
                {
                    "instrument_type": self.instrument_type,
                    "part_number": 2,
                    "note": "i Eb",
                    "pdf": self.pdf,
                },
            ],
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.part.get_absolute_url(),
            reverse(
                "sheetmusic:PartDetail",
                kwargs={"score_slug": self.pdf.score.slug, "slug": self.part.slug},
            ),
        )

    def test_pdf_file(self):
        """
        Checks that pdf_file has 1 page
        """
        pdf_stream = self.part.pdf_file()
        pdf_reader = PdfFileReader(pdf_stream)
        self.assertEqual(pdf_reader.getNumPages(), 1)

    def test_pdf_filename(self):
        """
        Checks that pdf_filename returns "99-luftballons-trombone-1.pdf"
        """
        score = ScoreFactory(title="99 Luftballons")
        pdf = PdfFactory(score=score)
        trombone = InstrumentTypeFactory(name="Trombone")
        part = PartFactory(pdf=pdf, instrument_type=trombone, part_number=1)
        self.assertEquals(part.pdf_filename(), "99-luftballons-trombone-1.pdf")

    def test_is_favorite_for(self):
        """
        Checks that is_favorite_for returns True when user has part as favorite and False when not.
        """
        user = UserFactory()
        self.part.refresh_from_db()
        self.assertFalse(self.part.is_favorite_for(user))
        FavoritePartFactory(user=user, part=self.part)
        self.assertTrue(self.part.is_favorite_for(user))


class FavoritePartTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.part = PartFactory()
        self.favorite_part = FavoritePartFactory(user=self.user, part=self.part)

    def test_to_str(self):
        self.assertEqual(str(self.favorite_part), f"{self.user}-{self.part}")

    def test_unique(self):
        """
        Checks that you can only have one FavoritePart for each combination of user and part.
        """
        with self.assertRaises(IntegrityError):
            FavoritePartFactory(user=self.user, part=self.part)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.favorite_part.get_absolute_url(),
            reverse("sheetmusic:ScoreView", kwargs={"slug": self.part.pdf.score.slug}),
        )


class EditFileTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.edit_file = EditFileFactory()

    def test_to_str(self):
        """`__str__` should be the edit file filename."""
        self.assertEqual(str(self.edit_file), self.edit_file.filename_original)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.edit_file.get_absolute_url(),
            reverse("sheetmusic:ScoreView", kwargs={"slug": self.edit_file.score.slug}),
        )


class SheetmusicBreadcrumbsTestSuite(TestMixin, TestCase):
    def test_normal(self):
        self.assertEqual(
            sheetmusic_breadcrumbs(),
            [Breadcrumb(reverse("sheetmusic:ScoreList"), "Alle notar")],
        )

    def test_score(self):
        score = ScoreFactory()
        self.assertEqual(
            sheetmusic_breadcrumbs(score=score),
            [
                Breadcrumb(
                    reverse("sheetmusic:ScoreList"),
                    "Alle notar",
                ),
                Breadcrumb(
                    reverse("sheetmusic:ScoreView", args=[score.slug]),
                    str(score),
                ),
            ],
        )

    def test_parts_update_index(self):
        score = ScoreFactory()
        self.assertEqual(
            sheetmusic_breadcrumbs(score=score, parts_update_index=True),
            [
                Breadcrumb(
                    reverse("sheetmusic:ScoreList"),
                    "Alle notar",
                ),
                Breadcrumb(
                    reverse("sheetmusic:ScoreView", args=[score.slug]),
                    str(score),
                ),
                Breadcrumb(
                    reverse("sheetmusic:PartsUpdateIndex", args=[score.slug]),
                    "Rediger stemmer",
                ),
            ],
        )


class ScoreViewTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def get_url(self):
        return reverse("sheetmusic:ScoreView", args=[self.score.slug])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_view_score(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_parts_in_context(self):
        user = UserFactory()
        part = PartFactory(pdf__score=self.score)
        self.client.force_login(user)
        context = self.client.get(self.get_url()).context
        self.assertEqual(list(context["parts"]), [part])

    def test_parts_favorite_in_context(self):
        user = UserFactory()
        part = PartFactory(pdf__score=self.score)
        FavoritePartFactory(user=user, part=part)
        self.client.force_login(user)
        context = self.client.get(self.get_url()).context
        self.assertEqual(list(context["parts_favorite"]), [part])

    def test_parts_instrument_group_in_context(self):
        instrument_type = InstrumentTypeFactory()
        user = UserFactory(instrument_type=instrument_type)
        part = PartFactory(pdf__score=self.score, instrument_type=instrument_type)
        self.client.force_login(user)
        context = self.client.get(self.get_url()).context
        self.assertEqual(list(context["parts_instrument_group"]), [part])

    def test_favorite_on_parts_in_context(self):
        user = UserFactory()
        FavoritePartFactory(user=user, part__pdf__score=self.score)
        self.client.force_login(user)
        context = self.client.get(self.get_url()).context
        self.assertTrue(list(context["parts"])[0].favorite)


class ScoreCreateTestSuite(TestMixin, TestCase):
    def test_create_score(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(reverse("sheetmusic:ScoreCreate"), {"title": "A score"})
        self.assertEqual(Score.objects.count(), 1)
        score = Score.objects.last()
        self.assertEqual(score.title, "A score")

    def test_requires_login(self):
        self.assertLoginRequired(reverse("sheetmusic:ScoreCreate"))


class ScoreUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def get_url(self):
        return reverse("sheetmusic:ScoreUpdate", args=[self.score.slug])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.change_score",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `change_score` permission.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            self.get_url(),
            {"title": "B score"},
        )
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_nav_tabs_in_context(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.get(self.get_url())
        self.assertEquals(
            response.context["nav_tabs"], nav_tabs_score_edit(self.score, user)
        )


class ScoreDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def get_url(self):
        return reverse("sheetmusic:ScoreDelete", args=[self.score.slug])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.delete_score",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete scores.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), {})
        self.assertRedirects(response, reverse("sheetmusic:ScoreList"))


class PartsUpdateIndexTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def get_url(self):
        return reverse("sheetmusic:PartsUpdateIndex", args=[self.score.slug])

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.add_part",
            "sheetmusic.change_part",
            "sheetmusic.delete_part",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to modify parts.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_context_data(self):
        pdf = PdfFactory(score=self.score)
        user = SuperUserFactory()
        self.client.force_login(user)
        context = self.client.get(self.get_url()).context
        self.assertEqual(list(context["pdfs"]), [pdf])
        self.assertEqual(context["score"], self.score)


class PartsUpdateTestSuite(TestMixin, TestCase):
    def create_post_data(self, data=[]):
        return create_formset_post_data(
            PartsUpdateFormset,
            defaults={
                "instrument_type": self.instrument_type.pk,
                "part_number": "",
                "note": "",
                "from_page": "1",
                "to_page": "1",
                "id": str(self.part.pk),
            },
            data=data,
        )

    def get_url(self, pdf=None):
        return reverse(
            "sheetmusic:PartsUpdate",
            args=[self.pdf.score.slug, self.pdf.slug]
            if not pdf
            else [pdf.score.slug, pdf.slug],
        )

    def setUp(self):
        self.score = ScoreFactory()
        self.instrument_type = InstrumentTypeFactory()
        self.pdf = PdfFactory(
            score=self.score,
            file=test_pdf_multipage(["Vanlig stemme", "Håndskrevet andrestemme"]),
        )
        self.part = PartFactory(pdf=self.pdf)

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.add_part",
            "sheetmusic.change_part",
            "sheetmusic.delete_part",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to modify parts.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accounts_for_both_score_slug_and_pdf_slug(self):
        """Should find the correct PDF for the given score."""
        different_score = ScoreFactory()
        different_pdf_same_slug = PdfFactory(score=different_score, slug=self.pdf.slug)

        self.client.force_login(SuperUserFactory())
        response = self.client.get(self.get_url(different_pdf_same_slug))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["object"], different_pdf_same_slug)

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.create_post_data())
        self.assertRedirects(
            response, reverse("sheetmusic:PartsUpdateIndex", args=[self.score.slug])
        )

    def test_modify(self):
        user = SuperUserFactory()
        other_instrument_type = InstrumentTypeFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"instrument_type": other_instrument_type.pk}]),
        )
        self.part.refresh_from_db()
        self.assertEqual(self.part.instrument_type, other_instrument_type)

    def test_add(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data(
                [
                    {},
                    {
                        "instrument_type": self.instrument_type.pk,
                        "part_number": "2",
                        "note": "håndskrevet",
                        "from_page": "2",
                        "to_page": "2",
                    },
                ]
            ),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 2)
        part = self.pdf.parts.last()
        self.assertEqual(part.instrument_type, self.instrument_type)
        self.assertEqual(part.part_number, 2)
        self.assertEqual(part.note, "håndskrevet")

    def test_delete(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 0)

    def test_modified_by_of_score_set_to_current_user(self):
        """Should set `modified_by` of the score to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.create_post_data())

        self.score.refresh_from_db()
        self.assertEqual(self.score.modified_by, user)


class PartsUpdateAllTestSuite(TestMixin, TestCase):
    def create_post_data(self, data=[]):
        return create_formset_post_data(
            PartsUpdateAllFormset,
            defaults={
                "instrument_type": self.instrument_type.pk,
                "part_number": "",
                "note": "",
                "from_page": "1",
                "to_page": "1",
                "pdf": str(self.pdf.pk),
                "id": str(self.part.pk),
            },
            data=data,
        )

    def get_url(self):
        return reverse("sheetmusic:PartsUpdateAll", args=[self.score.slug])

    def setUp(self):
        self.instrument_type = InstrumentTypeFactory()
        self.score = ScoreFactory()
        self.pdf = PdfFactory(
            score=self.score, file=test_pdf_multipage(["Instrument A", "Instrument B"])
        )
        self.part = PartFactory(pdf=self.pdf)

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.add_part",
            "sheetmusic.change_part",
            "sheetmusic.delete_part",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to modify parts.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.create_post_data())
        self.assertRedirects(
            response, reverse("sheetmusic:PartsUpdateIndex", args=[self.score.slug])
        )

    def test_modify(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"part_number": 2}]),
        )
        self.part.refresh_from_db()
        self.assertEqual(self.part.part_number, 2)

    def test_add(self):
        user = SuperUserFactory()
        new_instrument_type = InstrumentTypeFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data(
                [
                    {},
                    {
                        "instrument_type": new_instrument_type.pk,
                        "from_page": "2",
                        "to_page": "2",
                        "pdf": str(self.pdf.pk),
                    },
                ]
            ),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 2)
        part = self.pdf.parts.last()
        self.assertEqual(part.instrument_type, new_instrument_type)

    def test_delete(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 0)

    def test_modified_by_of_score_set_to_current_user(self):
        """Should set `modified_by` of the score to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.create_post_data())

        self.score.refresh_from_db()
        self.assertEqual(self.score.modified_by, user)


class PdfsUpdateTestSuite(TestMixin, TestCase):
    def create_post_data(self, data=[]):
        return create_formset_post_data(
            EditPdfFormset,
            defaults={
                "id": str(self.pdf.pk),
            },
            data=data,
        )

    def get_url(self):
        return reverse("sheetmusic:PdfsUpdate", args=[self.score.slug])

    def setUp(self):
        self.score = ScoreFactory()
        self.pdf = PdfFactory(score=self.score)

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.delete_pdf",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete PDFs.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.create_post_data())
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_delete(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.score.pdfs.count()
        self.assertEqual(count, 0)

    def test_modified_by_of_score_set_to_current_user(self):
        """Should set `modified_by` of the score to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.create_post_data())

        self.score.refresh_from_db()
        self.assertEqual(self.score.modified_by, user)


class PdfsUploadTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.flute = InstrumentTypeFactory(name="Fløyte", detection_keywords=["Fløyte"])
        self.clarinet = InstrumentTypeFactory(
            name="Klarinett", detection_keywords=["Klarinett"]
        )
        self.tuba = InstrumentTypeFactory(name="Tuba", detection_keywords=["Tuba"])
        self.euphonium = InstrumentTypeFactory(
            name="Eufonium", detection_keywords=["Eufonium"]
        )
        self.score = ScoreFactory()
        self.pdf_file = test_pdf_multipage(
            ["Tuba", "Eufonium"], name="Fløyte og klarinett.pdf"
        )
        self.test_data = {
            "files": self.pdf_file,
            "part_prediction": "filename",
            "plz_wait": True,
        }

    def get_url(self):
        return reverse("sheetmusic:PdfsUpload", args=[self.score.slug])

    def upload_pdf(self):
        return self.client.post(self.get_url(), self.test_data)

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(), "sheetmusic.add_pdf", "sheetmusic.add_part"
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to upload PDFs.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_redirect(self):
        self.client.force_login(SuperUserFactory())
        response = self.upload_pdf()
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_preserves_filename(self):
        """Should preserve the original filename."""
        self.client.force_login(SuperUserFactory())
        self.upload_pdf()
        pdf = Pdf.objects.last()
        self.assertEqual(pdf.filename_original, self.pdf_file.name)

    def test_upload_pdf_filename(self):
        self.client.force_login(SuperUserFactory())
        self.upload_pdf()
        self.assertEqual(self.score.pdfs.count(), 1)
        self.assertEqual(self.score.pdfs.last().parts.count(), 2)
        self.assertEqual(
            self.score.pdfs.last()
            .parts.get(instrument_type=self.flute)
            .instrument_type,
            self.flute,
        )
        self.assertEqual(
            self.score.pdfs.last()
            .parts.get(instrument_type=self.clarinet)
            .instrument_type,
            self.clarinet,
        )
        self.assertEqual(Part.objects.count(), 2)

    def test_upload_pdf_sheatless(self):
        self.client.force_login(SuperUserFactory())
        self.test_data["part_prediction"] = "sheatless"
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 1)
        self.assertEqual(Part.objects.count(), 2)
        self.assertEqual(
            Part.objects.get(instrument_type=self.euphonium).instrument_type,
            self.euphonium,
        )
        self.assertEqual(
            Part.objects.get(instrument_type=self.tuba).instrument_type, self.tuba
        )

    def test_upload_pdf_no_part_prediction(self):
        self.client.force_login(SuperUserFactory())
        self.test_data["part_prediction"] = "none"
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 1)
        self.assertEqual(Part.objects.count(), 0)

    def test_upload_pdf_undefined_part_prediction(self):
        self.client.force_login(SuperUserFactory())
        self.test_data["part_prediction"] = "qwertyuiopå"
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 0)
        self.assertEqual(Part.objects.count(), 0)

    def test_upload_multiple_pdfs(self):
        self.client.force_login(SuperUserFactory())
        self.test_data["files"] = [test_pdf(name="tuba.pdf") for _ in range(3)]
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 3)
        self.assertEqual(Part.objects.count(), 3)

    def test_error_if_one_or_more_files_not_pdf(self):
        """Should display a form error if one more files aren't PDFs."""
        self.client.force_login(SuperUserFactory())
        image = test_image()
        self.test_data["files"] = [test_pdf() for _ in range(3)] + [image]
        response = self.upload_pdf()
        self.assertFormError(
            response.context["form"],
            "files",
            f"{image.name}: Filending '.gif' ikkje lovleg.",
        )


class ScoreListTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        self.assertLoginRequired(reverse("sheetmusic:ScoreList"))


class PartPdfTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.part = PartFactory()

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse(
                "sheetmusic:PartPdf",
                args=[self.part.pdf.score.slug, self.part.slug],
            )
        )

    def test_returns_pdf(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(
            reverse(
                "sheetmusic:PartPdf",
                args=[self.part.pdf.score.slug, self.part.slug],
            )
        )
        self.assertEqual(response["content-type"], "application/pdf")


class FavoritePartPdfTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.favorite_part = FavoritePartFactory()
        self.user = self.favorite_part.user
        self.part = self.favorite_part.part

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse(
                "sheetmusic:FavoritePartPdf",
                args=[self.part.pdf.score.slug],
            )
        )

    def test_returns_pdf(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "sheetmusic:FavoritePartPdf",
                args=[self.part.pdf.score.slug],
            )
        )
        self.assertEqual(response["content-type"], "application/pdf")


class EditFilesUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()
        self.edit_file = EditFileFactory(score=self.score)

    def create_post_data(self, data=[]):
        return create_formset_post_data(
            EditEditFileFormset,
            defaults={
                "id": str(self.edit_file.pk),
            },
            data=data,
        )

    def get_url(self):
        return reverse("sheetmusic:EditFilesUpdate", args=[self.score.slug])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.change_editfile",
            "sheetmusic.delete_editfile",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete edit files.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.create_post_data())
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_delete(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.score.edit_files.count()
        self.assertEqual(count, 0)

    def test_modified_by_of_score_set_to_current_user(self):
        """Should set `modified_by` of the score to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.create_post_data())

        self.score.refresh_from_db()
        self.assertEqual(self.score.modified_by, user)


class EditFilesUploadTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()
        self.file = test_txt_file(name="Free World Fantasy.mscz")
        self.test_data = {"file": self.file}

    def get_url(self):
        return reverse("sheetmusic:EditFilesUpload", args=[self.score.slug])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.add_editfile",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to upload edit files.
        """
        self.client.force_login(self.score.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_redirect(self):
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url(), self.test_data)
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_preserves_filename(self):
        """Should preserve the original filename."""
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.test_data)
        edit_file = EditFile.objects.last()
        self.assertEqual(edit_file.filename_original, self.file.name)

    def test_upload_multiple_edit_files(self):
        """Should let you upload multiple edit files at the same time."""
        self.client.force_login(SuperUserFactory())
        self.client.post(
            self.get_url(),
            {"file": [test_txt_file(name="Sjøbanan.mscz") for _ in range(3)]},
        )
        self.assertEqual(EditFile.objects.count(), 3)

    def test_modified_by_of_score_set_to_current_user(self):
        """Should set `modified_by` of the score to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.test_data)

        self.score.refresh_from_db()
        self.assertEqual(self.score.modified_by, user)
