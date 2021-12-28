import os
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data
from web.settings import BASE_DIR

from .factories import FavoritePartFactory, PartFactory, PdfFactory, ScoreFactory
from .forms import EditPdfFormset, PartsUpdateAllFormset, PartsUpdateFormset
from .models import Part, Pdf, Score


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
            defaults={
                "name": "name",
                "from_page": "1",
                "to_page": "1",
                "id": str(self.part.pk),
            },
            formset_class=PartsUpdateFormset,
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
            defaults={
                "name": "name",
                "from_page": "1",
                "to_page": "1",
                "pdf": str(self.pdf.pk),
                "id": str(self.part.pk),
            },
            formset_class=PartsUpdateAllFormset,
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
            defaults={
                "id": str(self.pdf.pk),
            },
            formset_class=EditPdfFormset,
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
        self.test_data = {
            "files": open(
                os.path.join(BASE_DIR, "common", "test_data", "test.pdf"), "rb"
            ),
            "part_prediction": "filename",
            "plz_wait": True,
        }

    def upload_pdf(self):
        self.client.post(
            reverse("sheetmusic:PdfsUpload", args=[self.score.slug]),
            self.test_data,
        )

    def test_requires_login(self):
        self.assertLoginRequired(
            reverse("sheetmusic:PdfsUpload", args=[self.score.slug])
        )

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:PdfsUpload", args=[self.score.slug]),
            "sheetmusic.add_pdf",
            "sheetmusic.add_part",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            reverse("sheetmusic:PdfsUpload", args=[self.score.slug]),
            self.test_data,
        )
        self.assertRedirects(
            response, reverse("sheetmusic:ScoreView", args=[self.score.slug])
        )

    def test_upload_pdf_filename(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.upload_pdf()
        self.assertEqual(self.score.pdfs.count(), 1)
        self.assertEqual(self.score.pdfs.last().parts.count(), 1)
        self.assertEqual(self.score.pdfs.last().parts.last().name, "test")
        self.assertEqual(Part.objects.count(), 1)

    def test_upload_pdf_sheatless(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.test_data["part_prediction"] = "sheatless"
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 1)
        self.assertEqual(Part.objects.count(), 1)
        self.assertEqual(Part.objects.last().name, "Tuba")

    def test_upload_pdf_no_part_prediction(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.test_data["part_prediction"] = "none"
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 1)
        self.assertEqual(Part.objects.count(), 0)

    def test_upload_pdf_undefined_part_prediction(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.test_data["part_prediction"] = "qwertyuiopå"
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 0)
        self.assertEqual(Part.objects.count(), 0)

    def test_upload_multiple_pdfs(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.test_data["files"] = [
            open(os.path.join(BASE_DIR, "common", "test_data", "test.pdf"), "rb")
            for _ in range(3)
        ]
        self.upload_pdf()
        self.assertEqual(Pdf.objects.count(), 3)
        self.assertEqual(Part.objects.count(), 3)


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
