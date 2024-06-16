"""
test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """model test"""

    def test_create_user_with_email_succesful(self):
        """Test creating an user with an email is succesful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new user"""

        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(
                email, 'password123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises an ValueError"""

        with self.assertRaises(ValueError):
            password = 'testpass123'
            email = ''
            user = get_user_model().objects.create_user(
                email=email,
                password=password,
            )
    
    def test_create_superuser(self):
        """Test that creating a superuser."""

        email="123@example.com"
        password="123"

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
