from django.test import TestCase
from django.core import mail
from django.db import IntegrityError
from django.urls import reverse
from accounts.factories import UserFactory
from contact.factories import ContactCategoryFactory


class ContactCategoryTestCase(TestCase):
    def test_to_str(self):
        """Should be the category's name."""
        category = ContactCategoryFactory()
        self.assertEqual(str(category), category.name)

    def test_name_is_unique(self):
        """Category name should be unique."""
        name = "This is a name"
        ContactCategoryFactory(name=name)
        with self.assertRaises(IntegrityError):
            ContactCategoryFactory(name=name)

    def test_multiple_categories_with_same_email(self):
        """Multiple categories should be able to have the same email."""
        email = "test@taktlaus.no"
        a = ContactCategoryFactory(email=email)
        b = ContactCategoryFactory(email=email)
        self.assertEqual(a.email, b.email)


class ContactViewTestCase(TestCase):
    def setUp(self):
        self.category = ContactCategoryFactory()
        self.mail_data = {
            "name": "Bob",
            "email": "bob@bobbington.com",
            "subject": "Test",
            "category": self.category.name,
            "message": "Message test.",
        }

    def send_test_mail(self, to_self=False):
        self.client.post(
            reverse("contact"), {**self.mail_data, "send_to_self": to_self}
        )
        self.assertEqual(len(mail.outbox), 1)
        return mail.outbox[0]

    def test_correct_from_mail(self):
        """Should have the correct from mail."""
        email = self.send_test_mail()
        self.assertEqual(email.from_email, self.mail_data["email"])

    def test_to_mail_only_category_mail_if_not_send_to_self(self):
        """To mail should only be the category mail if `send_to_self` is false."""
        email = self.send_test_mail()
        self.assertEqual(email.to, [self.category.email])

    def test_to_mail_includes_self_mail_if_send_to_self(self):
        """To mail should include the submitted mail if `send_to_self` is true."""
        email = self.send_test_mail(to_self=True)
        self.assertIn(self.category.email, email.to)
        self.assertIn(self.mail_data["email"], email.to)

    def test_body_includes_name_and_message(self):
        """Email body should include the name and the message."""
        email = self.send_test_mail()
        self.assertIn(self.mail_data["name"], email.body)
        self.assertIn(self.mail_data["message"], email.body)

    def test_subject_includes_subject_and_category(self):
        """Email subject should include subject and category."""
        email = self.send_test_mail()
        self.assertIn(self.mail_data["subject"], email.subject)
        self.assertIn(self.category.name, email.subject)

    def test_initial(self):
        """Should initialize with username and email if logged in."""
        user = UserFactory(username="Bob", email="bob@bobbington.com")
        self.client.force_login(user)
        response = self.client.get(reverse("contact"))
        self.assertDictEqual(
            response.context["form"].initial,
            {"name": user.username, "email": user.email},
        )
