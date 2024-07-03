"""
Views for the recipe API.
"""

from rest_framework import viewsets # viewset are a class based view that provide operation for CRUD operation 
from rest_framework.authentication import TokenAuthentication # this authenticaiton is so that user provide a token in their request to prove their identity
from rest_framework.permissions import IsAuthenticated # permission class to allow access only to authenticated user

from core.models import Recipe # import the model

from recipe import serializers # to serialize classes Recipe instances


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all() # sets the default queryset for the viewset to all Recipe instances. This is used to list and detail views
    authentication_classes = [TokenAuthentication] # sets the authenticatoin class for the viewset
    permission_classes = [IsAuthenticated] # sets the persmission classes for the viewset. Only authenticated user are allow to access this viewset

    def get_queryset(self): 
        """Retrive recepie for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id') # this overrides the ger_queryset method to return only the recipe for the current authenticated user. this method is called when a list view is requested
    
    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class