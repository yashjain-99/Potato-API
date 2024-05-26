"""
Serializers for recipe API
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingredient
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags objects"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for tags objects"""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipe object"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id',
                  'title',
                  'time_minutes',
                  'price',
                  'link',
                  'tags',
                  'ingredients']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a recipe"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient
            )
            recipe.ingredients.add(ingredient_obj)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe"""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        recipe = super().update(instance, validated_data)
        auth_user = self.context['request'].user
        recipe.tags.clear()
        recipe.ingredients.clear()
        if(tags):
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(
                    user=auth_user,
                    **tag
                )
                recipe.tags.add(tag_obj)
        if(ingredients):
            for ingredient in ingredients:
                ingredient_obj, created = Ingredient.objects.get_or_create(
                    user=auth_user,
                    **ingredient
                )
                recipe.ingredients.add(ingredient_obj)
        recipe.save()
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe details view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipe"""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image': {
                'required': True
            }
        }
