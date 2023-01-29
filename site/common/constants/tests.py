from django.db import IntegrityError
from django.test import TestCase

from common.mixins import TestMixin

from .factories import ConstantFactory


class ConstantTestSuite(TestMixin, TestCase):
    def setUp(self) -> None:
        self.constant = ConstantFactory()

    def test_to_str(self):
        """`__str__` should be the constant's name."""
        self.assertEqual(str(self.constant), self.constant.name)

    def test_name_unique(self):
        """`name` should be unique."""
        with self.assertRaises(IntegrityError):
            ConstantFactory(name=self.constant.name)
