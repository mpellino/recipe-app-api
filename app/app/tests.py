"""
Sample test
"""
import os

from django.test import SimpleTestCase
from app import calc

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')


class CalcTests(SimpleTestCase):
    """Test the calc module."""

    def test_add_numbers(self):
        """Test adding numbers together."""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """Test subtracting numbers."""
        res = calc.subtract(8, 4)

        self.assertEqual(res, 4)
