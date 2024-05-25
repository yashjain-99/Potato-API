"""
URLS mapping for the recipe API
"""
from django.urls import (path, include)
# create routes for all the diff object available for that view
from rest_framework.routers import DefaultRouter

from recipe import views

app_name = 'recipe'
router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
