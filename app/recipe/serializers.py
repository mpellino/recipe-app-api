"""
Serializer for the recepie APIs
"""

from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recepies object"""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']

    def createRecipe(self, validated_data):
        """Create and return a recipe."""
        return Recipe().objects.create(**validated_data)
    
class RecipeDetailSerializer(RecipeSerializer): #Since RecipeDetailSerializer is an extention of RecipeSeralizer we can use the latter as baseclass
    """Serializer for recipe detail view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description'] # adding an extra field on top of the RecipeSerializer
