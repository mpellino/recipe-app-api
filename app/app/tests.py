"""
Sample test
"""
from django.test import SimpleTestCase
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
from app import calc

class CalcTest(SimpleTestCase):
    """test the calc module"""

    def test_add_numbers(self):
        """test adding numbers together"""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_number(self): 
        """test subtracting numbers."""
        res = calc.subtract(8,4)

        self.assertEqual(res,4)
