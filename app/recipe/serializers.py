"""
Serializer for the recepie APIs
"""

from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recepies object"""

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id']

    def createRecipe(self, validated_data):
        """Create and return a recipe."""
        return Recipe().objects.create(**validated_data)
