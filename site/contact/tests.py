from django.test import TestCase
from django.db import IntegrityError
from contact.factories import ContactCategoryFactory


class ContactCategoryTestCase(TestCase):
    def test_to_str(self):
        """Should be the category's name."""
        category = ContactCategoryFactory()
        self.assertEqual(str(category), category.name)

    def test_name_is_unique(self):
        """Should enforce uniqueness of the category name."""
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
