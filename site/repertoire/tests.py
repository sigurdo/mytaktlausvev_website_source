from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data

from .factories import RepertoireFactory, RepertoireEntryFactory
from .forms import RepertoireEntryUpdateFormset


class RepertoireListTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        self.assertLoginRequired(reverse("repertoire:RepertoireList"))


class RepertoireCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.test_data = {"title": "Repertoire"}

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
            formset_class=RepertoireEntryUpdateFormset,
            defaults={},
            data=data,
            subform_prefix="entries",
        )

    def get_url(self):
        return reverse("repertoire:RepertoireUpdate", args=[self.repertoire.pk])

    def setUp(self):
        self.repertoire = RepertoireFactory()
        self.entry = RepertoireEntryFactory(repertoire=self.repertoire)
        self.test_data = self.create_post_data(
            data=[{"score": self.entry.score.pk, "id": self.entry.pk}]
        )
        self.test_data["title"] = self.repertoire.title

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
        self.assertRedirects(response, self.get_url())
