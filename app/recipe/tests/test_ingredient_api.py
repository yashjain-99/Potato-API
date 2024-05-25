"""
Test for ingredient api
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


def create_user(email='user@example.com', password='testPass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


def detail_url(ingredient_id):
    """Return URL for a particular id"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class PublicIngredientApiTests(TestCase):
    """Test unaunthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieiving ingredient list"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test provate Ingredient API requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredient(self):
        """Test retrieve Ingredient list"""
        Ingredient.objects.create(user=self.user, name="IngredientA")
        Ingredient.objects.create(user=self.user, name="IngredientB")
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test retrive ingredient related to particular user"""
        other_user = create_user(
            email='other@example.com',
            password='pass123',
        )
        Ingredient.objects.create(user=self.user, name="IngredientA")
        Ingredient.objects.create(user=other_user, name="IngredientB")
        res = self.client.get(INGREDIENT_URL)
        ing = Ingredient.objects.filter(user=self.user)
        serializer = IngredientSerializer(ing, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_ingredient(self):
        """Test updating a Ingredient"""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Ingredient1')
        payload = {'name': 'Ingredient2'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Testing deleting a ingredient"""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='ingredient1')
        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())
