import os

from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data
from web.settings import BASE_DIR

from .factories import PartFactory, PdfFactory, ScoreFactory
from .models import Score, Pdf, Part

# Create your tests here.


class ScoreViewTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def test_requires_login(self):
        self.assertLoginRequired(reverse("sheetmusic:ScoreView", args=[self.score.pk]))

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:ScoreView", args=[self.score.pk]), "sheetmusic.view_score"
        )

    def test_view_score(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse("sheetmusic:ScoreView", args=[self.score.pk]))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ScoreUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def test_requires_login(self):
        self.assertLoginRequired(reverse("sheetmusic:ScoreUpdate", args=[self.score.pk]))

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:ScoreUpdate", args=[self.score.pk]), "sheetmusic.change_score"
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            reverse("sheetmusic:ScoreUpdate", args=[self.score.pk]), {"title": "B score"}
        )
        self.assertRedirects(response, reverse("sheetmusic:ScoreUpdate", args=[self.score.pk]))


class ScoreDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.score = ScoreFactory()

    def test_requires_login(self):
        self.assertLoginRequired(reverse("sheetmusic:ScoreDelete", args=[self.score.pk]))

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:ScoreDelete", args=[self.score.pk]), "sheetmusic.delete_score"
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse("sheetmusic:ScoreDelete", args=[self.score.pk]), {})
        self.assertRedirects(response, reverse("sheetmusic:ScoreList"))


class PartsUpdateTestSuite(TestMixin, TestCase):
    def create_post_data(self, forms):
        return create_formset_post_data(
            fields={
                "name": "name",
                "from_page": "1",
                "to_page": "1",
                "pdf": str(self.pdf.pk),
                "id": str(self.part.pk),
                "DELETE": "",
            },
            forms=forms,
        )

    def setUp(self):
        self.score = ScoreFactory()
        self.pdf = PdfFactory(score=self.score)
        self.part = PartFactory(pdf=self.pdf)
        self.test_data = self.create_post_data([])

    def test_requires_login(self):
        self.assertLoginRequired(reverse("sheetmusic:PartsUpdate", args=[self.score.pk]))

    def test_requires_permission(self):
        self.assertPermissionRequired(
            reverse("sheetmusic:PartsUpdate", args=[self.score.pk]),
            "sheetmusic.add_part",
            "sheetmusic.change_part",
            "sheetmusic.delete_part",
        )

    def test_success_redirect(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        response = self.client.post(
            reverse("sheetmusic:PartsUpdate", args=[self.score.pk]), self.test_data
        )
        self.assertRedirects(response, reverse("sheetmusic:PartsUpdate", args=[self.score.pk]))

    def test_modify(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("sheetmusic:PartsUpdate", args=[self.score.pk]),
            self.create_post_data([{"name": "another name"}]),
        )
        part = Part.objects.get(pk=self.part.pk)
        self.assertEqual(part.name, "another name")

    def test_add(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("sheetmusic:PartsUpdate", args=[self.score.pk]),
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
            reverse("sheetmusic:PartsUpdate", args=[self.score.pk]),
            self.create_post_data([{"DELETE": "on"}]),
        )
        count = self.pdf.parts.count()
        self.assertEqual(count, 0)


# class PdfsUpdateTestSuite(TestMixin, TestCase):


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
        self.assertPermissionRequired(reverse("sheetmusic:ScoreCreate"), "sheetmusic.add_score")


class PdfUploadTestSuite(TestMixin, TestCase):
    def test_upload_pdf(self):
        user = SuperUserFactory()
        score = ScoreFactory()
        self.client.force_login(user)
        with open(
            os.path.join(BASE_DIR, "common", "test_data", "test.pdf"), "rb"
        ) as file:
            self.client.post(
                reverse("sheetmusic:PdfsUpload", kwargs={"pk": score.pk}),
                {"files": file, "plz_wait": True},
            )
        self.assertEqual(score.pdfs.count(), 1)
