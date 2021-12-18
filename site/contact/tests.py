from django.test import TestCase
from django.conf import settings
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

    def send_test_mail(self):
        self.client.post(reverse("contact:ContactView"), self.mail_data)
        self.assertEqual(len(mail.outbox), 1)
        return mail.outbox[0]

    def test_from_mail(self):
        """Should be the address the server sends the mail from."""
        email = self.send_test_mail()
        self.assertEqual(email.from_email, settings.EMAIL_HOST_USER)

    def test_from_header(self):
        """Should include sender's name and email."""
        email = self.send_test_mail()
        self.assertEqual(
            email.extra_headers["From"],
            f'"{self.mail_data["name"]}" <{self.mail_data["email"]}>',
        )

    def test_sender_header(self):
        """Should be the address the server sends the mail from."""
        email = self.send_test_mail()
        self.assertEqual(email.extra_headers["Sender"], settings.EMAIL_HOST_USER)

    def test_to_mail_is_category_mail(self):
        """To mail should be the category mail."""
        email = self.send_test_mail()
        self.assertEqual(email.to, [self.category.email])

    def test_body_includes_name_mail_and_message(self):
        """Email body should include the name, the mail, and the message."""
        email = self.send_test_mail()
        self.assertIn(self.mail_data["name"], email.body)
        self.assertIn(self.mail_data["email"], email.body)
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
        response = self.client.get(reverse("contact:ContactView"))
        self.assertDictEqual(
            response.context["form"].initial,
            {"name": user.username, "email": user.email},
        )
