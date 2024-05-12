"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model  # Get ref to custom user models


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test email is notmalized"""
        sample_email = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@example.com','Test2@example.com'],
            ['TEST3@example.com','TEST3@example.com']
        ]
        for email, expected in sample_email:
            useer = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(useer.email, expected)