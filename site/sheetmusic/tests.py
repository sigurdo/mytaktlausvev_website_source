from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin

from .factories import ScoreFactory
from .models import Score

# Create your tests here.


class ScoreCreateTestCase(TestMixin, TestCase):
    def test_create_score(self):
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(reverse("createScore"), {"title": "A score"})

        self.assertEqual(Score.objects.count(), 1)
        score = Score.objects.last()
        self.assertEqual(score.title, "A score")

    def test_requires_login(self):
        self.assertLoginRequired(reverse("createScore"))

    def test_requires_permission(self):
        self.assertPermissionRequired(reverse("createScore"), "sheetmusic.add_score")


class PdfUploadTestCase(TestMixin, TestCase):
    def test_upload_pdf(self):
        user = SuperUserFactory()
        score = ScoreFactory()
        self.client.force_login(user)
        with open("test_data/test.pdf", "rb") as file:
            self.client.post(
                reverse("PdfsUpload", kwargs={"pk": score.pk}),
                {"files": file, "plz_wait": True},
            )
        self.assertEqual(score.pdfs.count(), 1)
