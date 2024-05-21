"""
Test for tags api
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(email='user@example.com', password='testPass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class PublicTagsApiTests(TestCase):
    """Test unaunthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieiving tags list"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test provate tags API requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieve tags list"""
        Tag.objects.create(user=self.user, name="Tag1")
        Tag.objects.create(user=self.user, name="Tag2")
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_list_limited_to_user(self):
        """Test list of tag is limited to auth user"""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        Tag.objects.create(user=other_user, name="Tag1")
        Tag.objects.create(user=self.user, name="Tag2")

        res = self.client.get(TAGS_URL)

        tag = Tag.objects.filter(user=self.user)
        serializer = TagSerializer(tag, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
