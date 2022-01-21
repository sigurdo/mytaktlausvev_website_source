import os
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data, test_image_gif_2x2, test_pdf

from .factories import FavoritePartFactory, PartFactory, PdfFactory, ScoreFactory
from .forms import EditPdfFormset, PartsUpdateAllFormset, PartsUpdateFormset
from .models import Part, Pdf, Score


class PdfTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.pdf = PdfFactory()

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


class ScoreViewTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_view_score(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(
            reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ScoreUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse("sheetmusic:ScoreUpdate", args=[self.score.slug])
        )

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:ScoreUpdate", args=[self.score.slug]),
            "sheetmusic.change_score",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            reverse("sheetmusic:ScoreUpdate", args=[self.score.slug]),
            {"title": "B score"},
        )
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )


class ScoreDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse("sheetmusic:ScoreDelete", args=[self.score.slug])
        )

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:ScoreDelete", args=[self.score.slug]),
            "sheetmusic.delete_score",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            reverse("sheetmusic:ScoreDelete", args=[self.score.slug]), {}
        )
        self.assertRedirects(response, reverse("sheetmusic:ScoreList"))


class PartsUpdateOverviewTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("sheetmusic:PartsUpdateIndex", args=[self.score.slug])

    def setUp(self):
        self.score = ScoreFactory()

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.add_part",
            "sheetmusic.change_part",
            "sheetmusic.delete_part",
        )


class PartsUpdateTestSuite(TestMixin, TestCase):
    def create_post_data(self, data):
        return create_formset_post_data(
            PartsUpdateFormset,
            defaults={
                "name": "name",
                "from_page": "1",
                "to_page": "1",
                "id": str(self.part.pk),
            },
            data=data,
        )

    def get_url(self):
        return reverse("sheetmusic:PartsUpdate", args=[self.score.slug, self.pdf.slug])

    def setUp(self):
        self.score = ScoreFactory()
        self.pdf = PdfFactory(score=self.score)
        self.part = PartFactory(pdf=self.pdf)
        self.test_data = self.create_post_data([])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.add_part",
            "sheetmusic.change_part",
            "sheetmusic.delete_part",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.test_data)
        self.assertRedirects(
            response, reverse("sheetmusic:PartsUpdateIndex", args=[self.score.slug])
        )

    def test_modify(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"name": "another name"}]),
        )
        part = Part.objects.get(pk=self.part.pk)
        self.assertEqual(part.name, "another name")

    def test_add(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data(
                [
                    {},
                    {
                        "name": "new name",
                        "from_page": "1",
                        "to_page": "1",
                    },
                ]
            ),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 2)
        part = self.pdf.parts.last()
        self.assertEqual(part.name, "new name")

    def test_delete(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 0)


class PartsUpdateAllTestSuite(TestMixin, TestCase):
    def create_post_data(self, data):
        return create_formset_post_data(
            PartsUpdateAllFormset,
            defaults={
                "name": "name",
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
        self.score = ScoreFactory()
        self.pdf = PdfFactory(score=self.score)
        self.part = PartFactory(pdf=self.pdf)
        self.test_data = self.create_post_data([])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        self.assertPermissionRequired(
            self.get_url(),
            "sheetmusic.add_part",
            "sheetmusic.change_part",
            "sheetmusic.delete_part",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(self.get_url(), self.test_data)
        self.assertRedirects(
            response, reverse("sheetmusic:PartsUpdateIndex", args=[self.score.slug])
        )

    def test_modify(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"name": "another name"}]),
        )
        part = Part.objects.get(pk=self.part.pk)
        self.assertEqual(part.name, "another name")

    def test_add(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data(
                [
                    {},
                    {
                        "name": "new name",
                        "from_page": "1",
                        "to_page": "1",
                        "pdf": str(self.pdf.pk),
                    },
                ]
            ),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 2)
        part = self.pdf.parts.last()
        self.assertEqual(part.name, "new name")

    def test_delete(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 0)


class PdfsUpdateTestSuite(TestMixin, TestCase):
    def create_post_data(self, data):
        return create_formset_post_data(
            EditPdfFormset,
            defaults={
                "id": str(self.pdf.pk),
            },
            data=data,
        )

    def setUp(self):
        self.score = ScoreFactory()
        self.pdf = PdfFactory(score=self.score)
        self.test_data = self.create_post_data([])

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse("sheetmusic:PdfsUpdate", args=[self.score.slug])
        )

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:PdfsUpdate", args=[self.score.slug]),
            "sheetmusic.delete_pdf",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            reverse("sheetmusic:PdfsUpdate", args=[self.score.slug]), self.test_data
        )
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_delete(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("sheetmusic:PdfsUpdate", args=[self.score.slug]),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.score.pdfs.count()
        self.assertEqual(count, 0)


class PdfsUploadTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()
        self.pdf_file = test_pdf()
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
        self.assertEqual(self.score.pdfs.last().parts.count(), 1)
        self.assertEqual(self.score.pdfs.last().parts.last().name, "test")
        self.assertEqual(Part.objects.count(), 1)

    def test_upload_pdf_sheatless(self):
        self.client.force_login(SuperUserFactory())
        self.test_data["part_prediction"] = "sheatless"
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 1)
        self.assertEqual(Part.objects.count(), 1)
        self.assertEqual(Part.objects.last().name, "Tuba")

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
        self.test_data["files"] = [test_pdf() for _ in range(3)]
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 3)
        self.assertEqual(Part.objects.count(), 3)

    def test_error_if_one_or_more_files_not_pdf(self):
        """Should display a form error if one more files aren't PDFs."""
        self.client.force_login(SuperUserFactory())
        image = test_image_gif_2x2()
        self.test_data["files"] = [test_pdf() for _ in range(3)] + [image]
        response = self.upload_pdf()
        self.assertFormError(
            response,
            "form",
            "files",
            f"{image.name}: Filtype {image.content_type} ikkje lovleg",
        )


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

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:ScoreCreate"), "sheetmusic.add_score"
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
